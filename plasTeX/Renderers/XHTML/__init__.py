#!/usr/bin/env python

import sys, os, re, codecs, plasTeX
from plasTeX.Renderers.PageTemplate import Renderer as _Renderer

class XHTML(_Renderer):
    """ Renderer for XHTML documents """

    fileExtension = '.html'
    imageTypes = ['.png','.jpg','.jpeg','.gif']
    vectorImageTypes = ['.svg']

    def cleanup(self, document, files, postProcess=None):
        res = _Renderer.cleanup(self, document, files, postProcess=postProcess)
        self.doJavaHelpFiles(document, version='1')
        self.doJavaHelpFiles(document, version='2')
        self.doEclipseHelpFiles(document)
        return res

    def processFileContent(self, document, s):
        s = _Renderer.processFileContent(self, document, s)

        # Force XHTML syntax on empty tags
        s = re.compile(r'(<(?:hr|br|img|link|meta)\b.*?)\s*/?\s*(>)', 
                       re.I|re.S).sub(r'\1 /\2', s)

        # Remove empty paragraphs
        s = re.compile(r'<p>\s*</p>', re.I).sub(r'', s)

        # Add a non-breaking space to empty table cells
        s = re.compile(r'(<(td|th)\b[^>]*>)\s*(</\2>)', re.I).sub(r'\1&nbsp;\3', s)
        
        return s
    
    def doEclipseHelpFiles(self, document, encoding='utf-8'):
        """ Generate files needed to use HTML as Eclipse Help """
        latexdoc = document.getElementsByTagName('document')[0]
        
        # Create table of contents
        if 'eclipse-contents' in self:
            toc = self['eclipse-contents'](latexdoc)
            f = codecs.open('eclipse-contents.xml', 'w', encoding)
            toc = re.sub(r'(<topic\b[^>]*[^/])\s*>\s*</topic>', r'\1 />', toc)
            f.write("<?xml version='1.0' encoding='utf-8' ?>\n")
            f.write(toc)
            f.close()

        # Create plugin file
        if 'eclipse-plugin' in self:
            toc = self['eclipse-plugin'](latexdoc)
            f = codecs.open('eclipse-plugin.xml', 'w', encoding)
            f.write("<?xml version='1.0' encoding='utf-8' ?>\n")
            f.write(toc)
            f.close()

    def doJavaHelpFiles(self, document, encoding='utf-8', version='2'):
        """ Generate files needed to use HTML as Java Help """
        latexdoc = document.getElementsByTagName('document')[0]
        version = str(version)
        
        # Create table of contents
        if ('javahelp-toc-'+version) in self:
            toc = self['javahelp-toc-'+version](latexdoc)
            toc = re.sub(r'(<tocitem\b[^>]*[^/])\s*>\s*</tocitem>', r'\1 />', toc)
            f = codecs.open('javahelp%s-toc.xml' % version, 'w', encoding)
            f.write("<?xml version='1.0' encoding='utf-8' ?>\n")
            f.write(toc)
            f.close()

        # Create index
        if ('javahelp-index-'+version) in self and latexdoc.index:
            idx = self['javahelp-index-'+version](latexdoc)
            idx = re.sub(r'(\n\s*)+', r'\n', idx)
            f = codecs.open('javahelp%s-index.xml' % version, 'w', encoding)
            f.write("<?xml version='1.0' encoding='utf-8' ?>\n")
            f.write(idx)
            f.close()

        # Create map file
        if ('javahelp-map-'+version) in self:
            idx = self['javahelp-map-'+version](latexdoc)
            idx = re.sub(r'(\n\s*)+', r'\n', idx)
            f = codecs.open('javahelp%s.jhm' % version, 'w', encoding)
            f.write("<?xml version='1.0' encoding='utf-8' ?>\n")
            f.write(idx)
            f.close()

        # Create helpset file
        if ('javahelp-helpset-'+version) in self:
            idx = self['javahelp-helpset-'+version](latexdoc)
            idx = re.sub(r'(\n\s*)+', r'\n', idx)
            f = codecs.open('javahelp%s.hs' % version, 'w', encoding)
            f.write("<?xml version='1.0' encoding='utf-8' ?>\n")
            f.write(idx)
            f.close()

Renderer = XHTML 
