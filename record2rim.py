# coding: utf-8

"""
Vérification de conformité d'une notice Marc XML
par rapport à une liste de zones autorisées


"""


def check_record_rim(xml_record, fields, format_marc="intermarc"):
    """
    xml_record : notice Marc XML
    fields : liste à plat des zones autorisées, 
             sous la forme ["008", "009", "245$a", etc.]
    Renvoie la liste des zones problématiques
    """
    liste_pbs = []
    for field in xml_record.xpath("*[@tag]"):
        tag = field.get("tag")
        if field.find("*[@code]") is None:
        # On a une zone sans sous-zone
        # Logiquement, c'est un controlfield
            if (tag not in fields
                and tag[0] != "9"):
                liste_pbs.append(tag)
        else:
        # On a des sous-zones
            for subfield in field.xpath("*[@code]"):
                code = subfield.get("code")
                path = f"{tag}${code}"
                if (path not in fields
                   and code != "w"):
                    if (tag[0] != "9" and format_marc != "unimarc"):
                        liste_pbs.append(path)
    return liste_pbs
