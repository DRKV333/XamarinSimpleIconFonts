This python script generates C# code for easy use of icon fonts in Xamarin.Forms markdown.

Normally, you'd need to do something like this:

```
<ImageButton Source="{FontImage &#xf0f3;, FontFamily=FaRegular}" />
```

But with a bit help from a custom markdown extension you can have:

```
<ImageButton Source="{i:FaRegular bell}" />
```

All you need is a mapping of icon names to unicode characters, which is what this script creates. Most icon fonts should have this info included in the font itself. The script uses the "fonttools" library to extract it.

In the examples folder you'll find code generated for FontAwesome and Google's Material Icons. Material Icons doesn't include meaningful glyph names, so I used a json file from here: https://github.com/jossef/material-design-icons-iconfont/blob/master/dist/fonts/MaterialIcons-Regular.json

To use the icons, just drop the generated code onto your shared project, and add the actual .ttf file as an EmbeddedResource.