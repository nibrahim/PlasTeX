#!/usr/bin/env python

"""
C.6.4 Verbatim

"""

from plasTeX import Macro, Environment, Command, sourcearguments, sourcechildren

class verbatim(Environment):

    def invoke(self, tex):
        """ Parse until we reach `\end{verbatim}' or `\endverbatim' """
        escape = self.ownerDocument.context.categories[0][0]
        bgroup = self.ownerDocument.context.categories[1][0]
        egroup = self.ownerDocument.context.categories[2][0]
        self.ownerDocument.context.push(self)
        self.parse(tex)
        self.ownerDocument.context.setVerbatimCatcodes()
        tokens = [self]

        # If we were invoke by a \begin{...} look for an \end{...}
        if self.macroMode == Environment.MODE_BEGIN:
            endpattern = list(r'%send%s%s%s' % (escape, bgroup, 
                                                self.nodeName, egroup))
        # If we were invoke as a command (i.e. \verbatim) look
        # for an end without groupings (i.e. \endverbatim)
        else:
            endpattern = list(r'%send%s' % (escape, self.nodeName))

        endlength = len(endpattern)
        # Iterate through tokens until the endpattern is found
        for tok in tex:
            tokens.append(tok)
            if len(tokens) >= endlength:
                if tokens[-endlength:] == endpattern:
                    tokens = tokens[:-endlength]
                    break

        end = self.ownerDocument.createElement(self.nodeName)
        if self.macroMode == Environment.MODE_BEGIN:
            end.macroMode = Environment.MODE_END

        tokens.append(end)
        self.ownerDocument.context.pop(self)
        return tokens

    def normalize(self, charsubs=[]):
        """ Normalize, but don't allow character substitutions """
        return Environment.normalize(self)


class VerbatimStar(verbatim):
    macroName = 'verbatim*'

class verb(Command):
    args = '*'

    def invoke(self, tex):
        """ Parse for matching delimiters """
        self.ownerDocument.context.push(self)
        self.parse(tex)
        self.ownerDocument.context.setVerbatimCatcodes()
        # See what the delimiter is
        for endpattern in tex:
            self.delimiter = endpattern
            break
        tokens = [self, endpattern]
        # Parse until this delimiter is seen again
        for tok in tex:
            tokens.append(tok)
            if tok == endpattern:
                break
        self.ownerDocument.context.pop(self)
        return tokens

    def digest(self, tokens):
        for endpattern in tokens:
            break
        for tok in tokens:
            if tok == endpattern:
                break
            self.appendChild(tok)

    def source(self):
        return '\\%s%s%s%s%s' % (self.nodeName, sourcearguments(self),
                                 self.delimiter, sourcechildren(self), 
                                 self.delimiter)
    source = property(source)

    def normalize(self, charsubs=[]):
        """ Normalize, but don't allow character substitutions """
        return Command.normalize(self)

