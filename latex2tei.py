#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import sys
# import locale
# from pdb import set_trace

__date__ = "09-10-2019"
__version__ = "1.0.3"
__author__ = "Marta Materni"

class UaLog(object):

    """
    print è attivato quando self.out+prn > 1
    out.==1  prn== 1 attivato
    out == 0 prn==1 NON attivato
    out == 0 prn==2 attivato
    """

    def __init__(self):
        self.used = False
        # ymd = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
        # ymd = str(datetime.datetime.today().strftime('%Y%m%d_%H_%M'))
        # self.path_log = path_log.replace('.log', f'_{ymd}.log')
        self.path_log = None
        self.out = None
        self.f = None

    def open(self, path_log, out=1):
        self.path_log = path_log
        self.out = out

    def log(self, s, prn=1):
        if self.out + prn > 1:
            print(s)
        if self.used is False:
            self.used = True
            self.f = open(self.path_log, "w")
            os.chmod(self.path_log, 0o666)
        self.f.write(s)
        self.f.write(os.linesep)
        self.f.flush()
        return self


# loginfo = Log()
logerr = UaLog()


TEI_DOC_BEG = """
<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml"
    schematypens="http://purl.oclc.org/dsdl/schematron"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
   <teiHeader>
      <fileDesc>
         <titleStmt>
            <title> </title>
            <author>Ausiàs March</author>
            <respStmt xml:id="XXX1">
               <name>Rosanna Cantavella, Universitat de València</name>
               <resp>Coordinator of LaTEX into TEI transformations</resp>
            </respStmt>
            <respStmt xml:id="XXX2">
               <name> </name>
               <resp>Changes LaTEX to TEI, coding volunteer</resp>
            </respStmt>
            <respStmt xml:id="XXX3">
               <name> </name>
               <resp> </resp>
            </respStmt>
            <respStmt xml:id="XXX4">
               <name>Llúcia Martín Pasqual, Universitat d"Alacant</name>
               <resp>Coordinator of manuscript transcription into LaTEX</resp>
            </respStmt>
         </titleStmt>
         <publicationStmt>
            <publisher>Pending publication</publisher>
            <date>Pending publication</date>
         </publicationStmt>
         <sourceDesc>
            <msDesc
               corresp="http://www.cervantesvirtual.com/obra/las-obras-del-famosissimo-philosofo-y-poeta-mossen-osias-marco-cauallero-valenciano-de-nacion-catalan--0/">
               <msIdentifier xml:id="a_Ed_1539_BnM">
                  <repository>Biblioteca Virtual Lluís Vives - Cervantes Virtual</repository>
               </msIdentifier>
               <msContents>
                  <msItem>
                     <rubric><locus></locus></rubric>
                  </msItem>
               </msContents>
            </msDesc>
         </sourceDesc>
      </fileDesc>
      <profileDesc>
         <langUsage>
            <language ident="CA">Catalan</language>
         </langUsage>
      </profileDesc>
      <encodingDesc>
         <editorialDecl>
            <p>This a TEI-XML adaptation out of the LaTEX version of Ausiàs March"s poems" synoptic
               edition, from all witnesses.</p>
         </editorialDecl>
      </encodingDesc>
   </teiHeader>
   <facsimile>
      <graphic url="" />
      </facsimile>
   <text>
      <body>
        <div type="poem" xml:id="div_XXX">
"""

TEI_DOC_END = """
         </div>
      </body>
   </text>
</TEI>
"""
BEGIN = "\\begin"
END = "\\end"
DOCUMENT = "document"
ESTROFA = "estrofa"
TORNADA = "tornada"

LG_ESTROFA = "cobla"
LG_TORNADA = "tornada"
LG_POEM = "poem"

TYPE_SEG = "hemistiquio"

NUMERO = "\\numero"
TEXTIT = "\\textit"
# PAG = "\\pagina"
# PAG_OP = "\\clauOberta"
# PAG_CL = "\\clauTancada"
TEXTSC = "\\textsc"
INTERLIN = "\\interlin"
TATXAT = "\\tatxat"

LDOTS = "\\ldots{}"
CED = "\\c{c}"
AAG = "\\`{a}"
AAC = "\\'{a}"
OA = "\\'{o}"
UA = "\\'{u}"


class Latex2Xml(object):

    def __init__(self, tex, xml, sgl, seg=0):
        self.path_tex = tex
        self.path_xml = xml
        self.sigla = sgl
        self.seg = int(seg)
        self.fxml = None
        file_name = os.path.basename(tex)
        lp = file_name.rfind('.')
        log_name = file_name[:lp]
        path_err = "%s.err.log" % (log_name)
        logerr.open(path_err)
        self.beg_lst = []
        self.l_num = 0
        self.lg_num = 0

    def prnxml(self, s):
        self.fxml.write(s)
        self.fxml.write(os.linesep)

    """
    def find_word(self, line, w, p0):
        line_lw = line.lower()
        w_lw = w.lower()
        pos = line_lw.find(w_lw, p0)
        return pos
    """

    # [2r]
    def find_pag(self, line):
        ok = False
        p0 = line.find('[')
        if p0 > -1:
            p1 = line.find(']', p0) + 1
            pgn = line[p0:p1]
            s = '<pb n="%s" facs="" />' % (pgn)
            self.prnxml(s)
            ok = True
        return ok

    def find_begin(self, line):
        begin_name = ''
        if line.find(BEGIN) > -1:
            p0 = line.find('{', 5) + 1
            p1 = line.find('}', p0)
            begin_name = line[p0:p1]
            if begin_name == DOCUMENT:
                self.prnxml(TEI_DOC_BEG.strip())
            elif begin_name == ESTROFA:
                self.lg_num += 1
                n = self.lg_num
                lgid = "%slg%s" % (self.sigla, n)
                s = "<lg type=\"%s\" n=\"%s\" xml:id=\"%s\" >" % (
                    LG_ESTROFA, n, lgid)
                self.prnxml(s)
            elif begin_name == TORNADA:
                self.lg_num += 1
                n = self.lg_num
                lgid = "%slg%s" % (self.sigla, n)
                s = "<lg type=\"%s\" n=\"%s\" xml:id=\"%s\" >" % (
                    LG_TORNADA, n, lgid)
                self.prnxml(s)
            else:
                self.prnxml("<ERROR>")
                logerr.log(line)
                logerr.log("BEGIN ERRRoR")
        return begin_name

    def find_end(self, line):
        end = ''
        if line.find(END) > -1:
            p0 = line.find('{', 2) + 1
            p1 = line.find('}', p0)
            end = line[p0:p1]
            beg_last = self.beg_lst[-1:][0]
            if end == beg_last:
                if end == DOCUMENT:
                    self.prnxml(TEI_DOC_END.strip())
                elif end == ESTROFA:
                    self.prnxml("</lg>")
                elif end == TORNADA:
                    self.prnxml("</lg>")
                else:
                    self.prnxml("</%s>" % (end))
        return end

    def find_numero(self, line):
        p1 = 0
        if line.find(NUMERO) > -1:
            p0 = line.find('{', 5) + 1
            p1 = line.find('}', p0) + 1
        return p1

    def parse_word(self, w):
        pt = w.find(TEXTIT)
        if pt > -1:
            pre = w[:pt]
            p0 = w.find("{", 5) + 1
            p1 = w.find("}", 5)
            arg = w[p0:p1]
            post = w[p1 + 1:]
            ap = '˝' if len(post) > 0 else ''
            abbr = "<abbr>%s%s%s</abbr>" % (pre, ap, post)
            expan = "<expan>%s%s%s</expan>" % (pre, arg, post)
            w = "<choice>%s%s</choice>" % (abbr, expan)

        pt = w.find(TEXTSC)
        if pt > -1:
            pre = w[:pt]
            p0 = w.find("{", 5) + 1
            p1 = w.find("}", 5)
            arg = w[p0:p1]
            w = "<c rend=\"large\" >%s</c>" % (arg)

        pt = w.find(INTERLIN)
        if pt > -1:
            pre = w[:pt]
            p0 = w.find("{", 5) + 1
            p1 = w.find("}", 5)
            arg = w[p0:p1]
            w = "<add place=\"interlinear\" >%s</add>" % (arg)

        pt = w.find(TATXAT)
        if pt > -1:
            pre = w[:pt]
            p0 = w.find("{", 5) + 1
            p1 = w.find("}", 5)
            arg = w[p0:p1]
            w = "<del rend=\"barred\" >%s</del>" % (arg)

        return w

    def parse_seg(self, line):
        line = line.replace(" ", " ", 1)
        line = line.replace(LDOTS, '.', -1)
        line = line.replace(CED, 'ç', -1)
        line = line.replace(AAG, 'à', -1)
        line = line.replace(AAC, 'á', -1)
        line = line.replace(OA, 'ó', -1)
        line = line.replace(UA, 'ú', -1)

        ws = line.split(" ")
        wls = []
        for w in ws:
            s = self.parse_word(w)
            wls.append(s)
        line = " ".join(wls)
        return line

    def parse_line(self, line, numero):
        line_text = line[numero:]
        pseg = line.find('/')
        if self.seg == 1 and pseg > -1:
            r01 = line_text.split('/')
            seg0 = r01[0].strip()
            seg1 = r01[1].strip()

            self.l_num += 1
            l_id = "%sl%s" % (self.sigla, self.l_num)
            xml = "<l n=\"%s\" xml:id=\"%s\">" % (self.l_num, l_id)
            self.prnxml(xml)

            l_id1 = "%sl%ss1" % (self.sigla, self.l_num)
            s = self.parse_seg(seg0)
            xml = "<seg type=\"%s\" xml:id=\"%s\">%s</seg>" % (
                TYPE_SEG, l_id1, s)
            self.prnxml(xml)

            l_id2 = "%sl%ss2" % (self.sigla, self.l_num)
            s = self.parse_seg(seg1)
            xml = "<seg type=\"%s\" xml:id=\"%s\">%s</seg>" % (
                TYPE_SEG, l_id2, s)
            self.prnxml(xml)
            self.prnxml("</l>")
        else:
            self.l_num += 1
            l_id = "%sl%s" % (self.sigla, self.l_num)
            l_op = "<l n=\"%s\" xml:id=\"%s\">" % (self.l_num, l_id)
            self.prnxml(l_op)
            s = self.parse_seg(line_text)
            self.prnxml(s)
            self.prnxml("</l>")

    def parse_tex(self):
        self.beg_lst = []
        f = None
        # code = locale.getpreferredencoding()
        try:
            f = open(self.path_tex, "rt")
            # f = open(self.path_tex, mode='r', encoding='utf-8')
            # f = open(self.path_tex, mode='r', encoding=code)
        except Exception as e:
            logerr.log("read file text")
            logerr.log(str(e))
            sys.exit(1)
        try:
            self.fxml = open(self.path_xml, "w")
            # self.fxml = open(self.path_xml, mode='w', encoding='utf-8')
            # self.fxml = open(self.path_xml, mode='w', encoding=code)
        except Exception as e:
            logerr.log("write file.xml")
            logerr.log(str(e))
            sys.exit(1)
        for line in f:
            line = line.strip()
            if line == '':
                continue
            line = line.replace('\ufeff', '', -1)
            line = line.replace('\t', ' ', -1)

            if self.find_pag(line):
                continue

            begin = self.find_begin(line)
            if begin != '':
                self.beg_lst.append(begin)
                continue

            end = self.find_end(line)
            if end != '':
                self.beg_lst.pop()
                continue

            numero = self.find_numero(line)
            if numero > 0:
                self.parse_line(line, numero)
        f.close()
        self.fxml.close()
        os.chmod(self.path_xml, 0o666)


def do_main(path_tex, path_xml, sgl, seg):
    txtv = Latex2Xml(path_tex, path_xml, sgl, seg)
    txtv.parse_tex()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    parser.add_argument('-t',
                        dest="tex",
                        required=True,
                        metavar="",
                        help="-t <file tex>")
    parser.add_argument('-x',
                        dest="xml",
                        required=True,
                        metavar="",
                        help="-x <file xml>")
    parser.add_argument('-s',
                        dest="sgl",
                        required=True,
                        metavar="",
                        help="-s <sigla>")
    parser.add_argument('-g',
                        dest="seg",
                        required=False,
                        metavar="",
                        default=0,
                        help="-g [0/1] 0) disable seg  1) enable seg)  default 0")
    args = parser.parse_args()
    if args.tex == args.xml:
        print("Name File output errato")
        sys.exit(0)
    do_main(args.tex, args.xml, args.sgl, args.seg)
