from django.utils.html import strip_tags  

def truncate_content(content, num_words=100):  
    text = strip_tags(content)  # 去掉 HTML 标签
    text =text.replace("&nbsp","") 
    text =text.replace("&hellip;","") 
    text =text.replace("&rdquo;","") 
    text =text.replace("&ldquo;","")
    if len(text)>100:
        text = text[:100] +"......"
    else:
        text = text[:100] 

    return text