# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------

import codecs as codecs
import xml.dom.minidom as minidom

#-------------------------------------------------------------------------------

nodeTypes = {
    "ELEMENT_NODE":1,
    "ATTRIBUTE_NODE":2,
    "TEXT_NODE":3,
    "COMMENT_NODE":8,
    "DOCUMENT_NODE":9,
    "DOCTYPE_NODE":10
    };

#-------------------------------------------------------------------------------

def clearText(text):
    return (text.replace("\n","").replace("\t","").replace(" ",""));
# clearText()

#-------------------------------------------------------------------------------

def copyNode(xmlDoc,node):
    nodeCopy = xmlDoc.createElement(node.nodeName);
    if (node.hasAttributes()):
        for (key,value) in (node.attributes.items()):
            nodeCopy.setAttribute(key,value);
        # for (key,value)
    else:
        pass;
    if (node.hasChildNodes()):
        for (subnode) in (node.childNodes):
            if (subnode.nodeType == nodeTypes["ELEMENT_NODE"]):
                nodeCopy.appendChild(copyNode(xmlDoc,subnode));
            elif (subnode.nodeType == nodeTypes["TEXT_NODE"]):
                if (clearText(subnode.nodeValue) != ""):
                    nodeCopy.appendChild(subnode);
                else:
                    pass;
            else:
                pass;
        # for (subnode)
    else:
        pass;
    return (nodeCopy);
# copyNode()

#-------------------------------------------------------------------------------

def getDocType(xmlDoc):
    if (xmlDoc.doctype):
        return (minidom.getDOMImplementation().createDocumentType(xmlDoc.doctype.name,xmlDoc.doctype.publicId,xmlDoc.doctype.systemId));
    else:
        return (None);
# getDocType()

#-------------------------------------------------------------------------------

def copyDoc(xmlDoc):
    if (xmlDoc.doctype): # if the xml document has a doctype node defined
        xmlDocTmp = minidom.Document();
        if (xmlDoc.hasChildNodes()):
            xmlDocTmp.appendChild(copyNode(xmlDoc,xmlDoc.documentElement));
        else:
            pass;
        xmlDocCopy = minidom.getDOMImplementation().createDocument(xmlDoc.documentElement.namespaceURI,xmlDoc.documentElement.tagName,getDocType(xmlDoc));
        xmlDocCopy.replaceChild(xmlDocTmp.documentElement,xmlDocCopy.documentElement);
    else:
        xmlDocCopy = minidom.Document();
        if (xmlDoc.hasChildNodes()):
            xmlDocCopy.appendChild(copyNode(xmlDoc,xmlDoc.documentElement));
        else:
            pass;
    return (xmlDocCopy);
# copyDoc()

#-------------------------------------------------------------------------------

def loadDoc(xmlDocName):
    return (copyDoc(minidom.parse(xmlDocName)));
# loadDoc()

#-------------------------------------------------------------------------------

def writeDoc(xmlDoc,fileName):
    f = codecs.open(filename=fileName,mode="w",encoding="utf-8");
    f.write(xmlDoc.toprettyxml(indent="\t",newl="\n",encoding="UTF-8").decode(encoding="utf-8"));
    # N.B. (by Luka Tolitch, on 2014-05-16, at 11:00):
    # To set the "encoding" attribute value in the declaration node of the xml document (i.e. in the "<?xml ... ?> node),
    # the "encoding" argument has to be specified in the ".toxml()" and ".toprettyxml()" xml string methods.
    # This, however, forces these methods to return a "bytes" immutable sequence type object,
    # that has to be decoded back to a "string" representation, using the standard bytes method ".decode()",
    # the "encoding" argument of which should, in principle, agree with that given to the one of the xml string methods above.
    f.close();
# writeDoc()

#-------------------------------------------------------------------------------

##if __name__ == "__main__":
##
##    d = loadDoc("examples/index.html");
##    print(d.toprettyxml());
##    writeDoc(d,"examples/index_copied_01.html");