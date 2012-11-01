def Indent( elem, level=0, indent='    ' ):
    """
    Function used to 'prettify' output xml from cElementTree's tree.getroot() 
    method into lines so it's easily read.
    """
    i = "\n" + level * indent
    if len( elem ):
        if not elem.text or not elem.text.strip():
            elem.text = i + indent
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            Indent( elem, level + 1, indent )
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and ( not elem.tail or not elem.tail.strip() ):
            elem.tail = i