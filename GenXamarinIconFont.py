from fontTools.ttLib.ttFont import TTFont
import sys
import os
import json

name, ext = os.path.splitext(sys.argv[1])
if ext == ".json":
	with open(sys.argv[1]) as f:
		names = json.load(f)
else:
	font = TTFont(sys.argv[1])
	names = {}
	for t in font["cmap"].tables:
		for k, v in t.cmap.items():
			names[v] = format(k, "04x")

template = """using System;
using System.Collections.Generic;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;
ATTRHERE
namespace NSHERE
{
    [AcceptEmptyServiceProvider]
    [ContentProperty("Glyph")]
    internal class NAMEHERE : IMarkupExtension<ImageSource>
    {
        private static readonly Dictionary<string, string> glyphs = new Dictionary<string, string>()
        {
STUFFHERE
        };

        public string Glyph { get; set; }
        public Color Color { get; set; }

        [TypeConverter(typeof(FontSizeConverter))]
        public double Size { get; set; } = (double)FontImageSource.SizeProperty.DefaultValue;

        public ImageSource ProvideValue(IServiceProvider serviceProvider) => new FontImageSource()
        { 
            FontFamily = "NAMEHERE",
            Glyph = glyphs[Glyph],
            Color = Color,
            Size = Size
        };

        object IMarkupExtension.ProvideValue(IServiceProvider serviceProvider) => ProvideValue(serviceProvider);
    }
}"""

stuff = ""

for k, v in names.items():
	stuff = stuff + f"            [\"{k}\"] = \"\\u{v}\",\n"

attr = f"\n[assembly: ExportFont(\"{os.path.basename(sys.argv[1])}\", Alias = \"NAMEHERE\")]\n" if ext != ".json" else ""

template = template.replace("ATTRHERE", attr).replace("NSHERE", sys.argv[2]).replace("NAMEHERE", sys.argv[3]).replace("STUFFHERE", stuff)

print(template)