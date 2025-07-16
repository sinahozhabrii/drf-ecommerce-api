def get_cloudinary_image_obj(instance,as_html=False,width=800,height=450,field_name='image'):

    if not hasattr(instance,field_name):
        return ""
    image_obj = getattr(instance,field_name)
    if not image_obj:
        return ""

    image_options = {
        'width':width,
        'height':height
    }
    if as_html:
        return image_obj.image(**image_options)
    url = image_obj.build_url(**image_options)
    return url