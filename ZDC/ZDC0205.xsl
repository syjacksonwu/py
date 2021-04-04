<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="2.0" 
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
 >
<!-- http://www.w3.org/1999/XSL/Format-->


<xsl:template  match="/">
 <html>
  <head>
    <title>ZDC<xsl:value-of select="ZDC/IDENT/VERSION-TYP"/>: <xsl:value-of select="ZDC/IDENT/DATEINAME"/></title>
  </head>
  <body>
   <H1>Steuergeräte-Zieldatencontainer  (Typ <xsl:value-of select="ZDC/IDENT/VERSION-TYP"/>)</H1>
   <p/>
   <xsl:apply-templates select="ZDC/IDENT"/>
   <xsl:apply-templates select="ZDC/INFO"/>
   <xsl:apply-templates select="ZDC/VORSCHRIFT/VERWEISE"/>
   <xsl:apply-templates select="ZDC/VORSCHRIFT/DIREKT/DIAGN"/>
   <xsl:apply-templates select="ZDC/VORSCHRIFT/DIREKT/LOGINID"/>
   <xsl:apply-templates select="ZDC/VORSCHRIFT/DIREKT/TABELLEN/VARIABLEN"/>
   <xsl:apply-templates select="ZDC/VORSCHRIFT/DIREKT/TABELLEN/REFERENZ"/>
   <xsl:apply-templates select="ZDC/VORSCHRIFT/DIREKT/TABELLEN/REFHSC"/>
   <xsl:apply-templates select="ZDC/VORSCHRIFT/DIREKT/TABELLEN/TABELLE"/>
   <xsl:apply-templates select="ZDC/VORSCHRIFT/DIREKT/DATENBEREICHE"/>
   <p>Stylesheet Version 1.1</p>
  </body>
 </html>
</xsl:template>

<xsl:template match="ZDC/IDENT">
 <table border="3">
  <caption align ="left"><b>Datei</b></caption>
  <TR>
   <TD>Dateiname</TD>
   <TD><xsl:apply-templates select="DATEINAME"/></TD>
  </TR>
  <TR>
   <TD>Dateiid</TD>
   <TD><xsl:apply-templates select="DATEIID"/></TD>
  </TR>
  <TR>
   <TD>Version</TD>
   <TD><xsl:value-of select="VERSION-INHALT"/></TD>
  </TR>
  <TR>
   <TD>Datum</TD>
   <TD><xsl:value-of select="DATUM"/></TD>
  </TR>
  <TR>
   <TD>Beschreibung</TD>
   <TD><xsl:value-of select="BESCHREIBUNG"/></TD>
  </TR>
  <TR>
   <TD>Checksumme</TD>
   <TD><xsl:value-of select="CNT-CHECKSUMME"/></TD>
  </TR>
 </table>
 <hr />
</xsl:template>

<xsl:template match="VARNAME">
 <xsl:attribute name="bgcolor">#EEE0EE</xsl:attribute>
  <xsl:value-of select="."/>
</xsl:template>

<xsl:template match="DATEINAME">
 <xsl:attribute name="bgcolor">#EEEEFF</xsl:attribute>
  <xsl:value-of select="."/>
</xsl:template>

<xsl:template match="DATEIID">
 <xsl:attribute name="bgcolor">#EEEEFF</xsl:attribute>
  <xsl:value-of select="."/>
</xsl:template>

<xsl:template match="DATEN-NAME">
 <xsl:attribute name="bgcolor">#EEEEEE</xsl:attribute>
  <xsl:value-of select="."/>
</xsl:template>

<xsl:template match="FEHLER">
 <xsl:attribute name="bgcolor">#FF0000</xsl:attribute>
  <xsl:value-of select="."/>
</xsl:template>

<xsl:template match="UNGUELTIG">
 <xsl:attribute name="bgcolor">#FEFE00</xsl:attribute>
  <xsl:value-of select="."/>
</xsl:template>

<xsl:template match="UEBERSPRINGEN">
 <xsl:attribute name="bgcolor">#EE00EE</xsl:attribute>
  <xsl:value-of select="."/>
</xsl:template>


<xsl:template match="VERWEISE">
 <table border="3">
  <caption align ="left"><b>Verweise</b></caption>
  <TR>
   <TD/>
   <TD>Dateiname</TD>
  </TR>
  <xsl:for-each select="DATEINAME">
   <TR>
    <TD><xsl:value-of select="position()"/></TD>
    <TD><xsl:apply-templates select="."/></TD>
   </TR>
  </xsl:for-each>
 </table>
 <hr />
</xsl:template>


<xsl:template match="ADRESSEN">
 <table border="3">
  <caption align ="left"><b>Ansprechpartner</b></caption>
  <tr>
   <td/>
   <xsl:for-each select="ADRESSE">
    <td><xsl:value-of select="position()"/></td>
   </xsl:for-each>
  </tr>
  <tr>
   <td>Firma</td>
   <xsl:for-each select="ADRESSE">
    <td><xsl:value-of select="FIRMA"/></td>
   </xsl:for-each>
  </tr>
  <tr>
   <td>Name</td>
   <xsl:for-each select="ADRESSE">
    <td><xsl:value-of select="MITARBEITER"/></td>
   </xsl:for-each>
  </tr>
  <tr>
   <td>Funktion</td>
   <xsl:for-each select="ADRESSE">
    <td><xsl:value-of select="FUNKTION"/></td>
   </xsl:for-each>
  </tr>
  <tr>
   <td>Telefon</td>
   <xsl:for-each select="ADRESSE">
    <td><xsl:value-of select="TELEFON"/></td>
   </xsl:for-each>
  </tr>
  <tr>
   <td>Handy</td>
   <xsl:for-each select="ADRESSE">
    <td><xsl:value-of select="MOBILE"/></td>
   </xsl:for-each>
  </tr>
  <tr>
   <td>Fax</td>
   <xsl:for-each select="ADRESSE">
    <td><xsl:value-of select="FAX"/></td>
   </xsl:for-each>
  </tr>
  <tr>
   <td>Email</td>
   <xsl:for-each select="ADRESSE">
    <td><xsl:value-of select="EMAIL"/></td>
   </xsl:for-each>
  </tr>
 </table>
 <hr />
</xsl:template>

<xsl:template match="DIAGN">
 <table border="3">
  <caption align ="left"><b>Kommunikation</b></caption>
  <xsl:if test="VERWSTELLE!=''">
   <TR>
    <TD>Verwendungsstelle</TD>
    <TD><b><xsl:value-of select="VERWSTELLE"/></b></TD>
   </TR>
  </xsl:if>
  <TR>
   <TD>Diagnosebus</TD>
   <TD><xsl:value-of select="BUS"/></TD>
  </TR>
  <TR>
   <TD>Diagnoseadresse</TD>
   <TD><xsl:value-of select="ADR"/></TD>
  </TR>
  <xsl:if test="KWP!=''">
    <TR>
     <TD>Diagnoseprotokoll</TD>
     <TD><xsl:value-of select="KWP"/></TD>
    </TR>
  </xsl:if>
  <xsl:if test="TP!=''">
    <TR>
     <TD>Transportprotokoll</TD>
     <TD><xsl:value-of select="TP"/></TD>
    </TR>
  </xsl:if>
  <xsl:if test="DIAGN/ADR!=''">
   <TR>
    <TD>Subbusse</TD>
    <TD><xsl:apply-templates select="DIAGN"/></TD>
   </TR>
  </xsl:if>
 </table>
 
<hr />
</xsl:template>

<xsl:template match="LOGINID">
  <xsl:if test=".!=''">
   <caption align ="left"><b>Login</b></caption>
   <table border="3">
     <TR>
      <TD>
         <xsl:attribute name="bgcolor">#FFFF00</xsl:attribute>
        Globale Login-ID
      </TD>
      <TD><b><xsl:value-of select="."/></b></TD>
     </TR>
    </table>
  </xsl:if>
 
<hr />
</xsl:template>

<xsl:template match="VARIABLEN">
 <table border="3">
  <caption align ="left"><b>Variablen</b></caption>
  <TR>
   <TD/>
   <TD>Name</TD>
   <TD>Typ</TD>
   <TD>min. Wert</TD>
   <TD>max. Wert</TD>
  </TR>
  <xsl:for-each select="VARIABLE">
   <xsl:variable name="varDATpos"><xsl:value-of select="position()"/></xsl:variable>
   <TR>
    <xsl:if test="$varDATpos mod 2 = 1"><xsl:attribute name="bgcolor">#EEFFEE</xsl:attribute></xsl:if>
    <TD><xsl:value-of select="position()"/></TD>
    <TD><xsl:apply-templates select="VARNAME"/></TD>
    <TD><xsl:value-of select="VARTYP"/></TD>
    <TD><xsl:value-of select="VARMINWERT"/></TD>
    <TD><xsl:value-of select="VARMAXWERT"/></TD>
   </TR>
  </xsl:for-each>
 </table>
 <xsl:apply-templates select="DIAGN"/>
<hr />
</xsl:template>

<xsl:template match="ZDC/VORSCHRIFT/DIREKT/TABELLEN/REFERENZ">
 <table border="3">
  <caption align ="left"><b>PR-Familien und -Nummern</b></caption>
  <TR>
    <xsl:attribute name="bgcolor">#EEEEEE</xsl:attribute>
    <TD>PRFAM</TD>
    <TD>PRNR</TD>
  </TR>
  <xsl:for-each select="REFFAM">
     <TR>
       <TD>
         <xsl:attribute name="bgcolor">#EEFFEE</xsl:attribute>
         <xsl:value-of select="FAMNR"/>
       </TD>       
       <xsl:for-each select="PRNR">
         <TD>
           <xsl:value-of select="."/>
         </TD>
       </xsl:for-each>
     </TR>
  </xsl:for-each>
 </table>
<hr />
</xsl:template>

<xsl:template match="ZDC/VORSCHRIFT/DIREKT/TABELLEN/REFHSC">
 <table border="3">
  <caption align ="left"><b>Herstellerkennzeichen</b></caption>
  <TR>
    <xsl:attribute name="bgcolor">#EEEEEE</xsl:attribute>
    <TD>HSC</TD>
  </TR>
  <xsl:for-each select="HSC">
     <TR>
       <TD>
         <xsl:attribute name="bgcolor">#EEFFEE</xsl:attribute>
         <xsl:value-of select="."/>
       </TD>       
     </TR>
  </xsl:for-each>
 </table>
<hr />
</xsl:template>

<xsl:template match="ZDC/VORSCHRIFT/DIREKT/DATENBEREICHE">
 <table border="3">
  <caption align ="left"><b>Daten</b></caption>
  <xsl:for-each select="DATENBEREICH">
   <xsl:variable name="varDATpos"><xsl:value-of select="position()"/></xsl:variable>
   <tr>
    <xsl:if test="$varDATpos mod 2 = 1"><xsl:attribute name="bgcolor">#EEFFEE</xsl:attribute></xsl:if>
    <td>
     <xsl:attribute name="rowspan"><xsl:value-of select="1+count(DATEN)"/></xsl:attribute>
     <xsl:apply-templates select="DATEN-NAME"/>
    </td>
    <td>Format: <xsl:value-of select="DATEN-FORMAT-NAME"/></td>
    <xsl:choose>
      <xsl:when test="KANAL!=''">
        <td>Kanal:<xsl:value-of select="KANAL"/></td>
      </xsl:when>
      <xsl:otherwise>
               <td>Adresse:<xsl:value-of select="START-ADR"/></td>
      </xsl:otherwise>
    </xsl:choose>
    <td>Laenge:<xsl:value-of select="GROESSE-DEKOMPRIMIERT"/></td>
   </tr>
   <xsl:for-each select="DATEN">
    <tr>
     <xsl:if test="$varDATpos mod 2 = 1"><xsl:attribute name="bgcolor">#EEFFEE</xsl:attribute></xsl:if>
     <td  colspan="3"><xsl:value-of select="."/></td>
    </tr>
   </xsl:for-each>
  </xsl:for-each>
 </table>
 <hr />
</xsl:template>

<xsl:template match="TABELLE">
 <table border="3">
  <caption align ="left"><b> <xsl:value-of select="TEXT"/></b></caption>


  <!-- 1. Zeile -->
  <tr>
   <xsl:attribute name="bgcolor">#FFAA00</xsl:attribute>
   <xsl:choose>
    <xsl:when test="MODUS='A'"><td>ANPASSUNG</td><td><xsl:value-of select="MODUSTEIL"/></td><td/><td  align = "right">Kanal</td></xsl:when>
    <xsl:when test="MODUS='C'"><td>CODIERUNG</td><td><xsl:value-of select="ZAHLENBASIS"/></td><td/><td  align = "right">Stelle</td></xsl:when>
    <xsl:when test="MODUS='F'"><td>UPDATEPROGRAMMIERUNG</td><td><xsl:value-of select="MODUSTEIL"/></td><td/><td  align = "right">Datei</td></xsl:when>
    <xsl:when test="MODUS='P'"><td>PROGRAMMIERUNG</td><td><xsl:value-of select="MODUSTEIL"/></td><td/><td  align = "right">Speicherzelle</td></xsl:when>
    <xsl:when test="MODUS='K'"><td>KALIBRIERUNG</td><td><xsl:value-of select="MODUSTEIL"/>&#160;ServiceID:&#160;<xsl:value-of select="SERVICEID"/>&#160;RDIDENTIFIER:&#160;<xsl:value-of select="RDIDENTIFIER"/></td><td/><td  align = "right">Stelle</td></xsl:when>
   </xsl:choose>

   <xsl:for-each select="KOPF/ZDE">
    <xsl:variable name="varSTELLEpos"><xsl:value-of select="position()"/></xsl:variable>
    <td  align = "center">
     <xsl:if test="$varSTELLEpos mod 2 = 1"><xsl:attribute name="bgcolor">#FFEEEE</xsl:attribute></xsl:if>
     <xsl:if test="$varSTELLEpos mod 2!= 1"><xsl:attribute name="bgcolor">#FFFFFF</xsl:attribute></xsl:if>
     
     <xsl:attribute name="colspan"><xsl:value-of select="count(ZDBYTE)"/></xsl:attribute>
      <xsl:choose>
      <xsl:when test="../../MODUS='C' and ../../ZAHLENBASIS='10'">
       <xsl:choose>
        <xsl:when test="ZDSTELLE='0'">1er</xsl:when>
        <xsl:when test="ZDSTELLE='1'">10er</xsl:when>
        <xsl:when test="ZDSTELLE='2'">100er</xsl:when>
        <xsl:when test="ZDSTELLE='3'">1000er</xsl:when>
        <xsl:when test="ZDSTELLE='4'">10000er</xsl:when>
        <xsl:when test="ZDSTELLE='5'">100000er</xsl:when>
        <xsl:when test="ZDSTELLE='6'">1000000er</xsl:when>
        <xsl:when test="ZDSTELLE='7'">10000000er</xsl:when>
        <xsl:when test="ZDSTELLE='8'">100000000er</xsl:when>
        <xsl:when test="ZDSTELLE='9'">1000000000er</xsl:when>
       </xsl:choose>
      </xsl:when>

      <xsl:when test="../../MODUS='C' and ../../ZAHLENBASIS='256'">
       <xsl:choose>
        <xsl:when test="ZDSTELLE='0'">Wert 1hex</xsl:when>
        <xsl:when test="ZDSTELLE='1'">Wert 100hex</xsl:when>
        <xsl:when test="ZDSTELLE='2'">Wert 10000hex</xsl:when>
       </xsl:choose>
      </xsl:when>
      <xsl:otherwise><xsl:value-of select="ZDSTELLE"/></xsl:otherwise>
     </xsl:choose>
    </td>
   </xsl:for-each>
  </tr>
  
  <!-- 2. Zeile -->
   <tr>    
    <xsl:attribute name="bgcolor">#EEEEEE</xsl:attribute>
    
    <td>Login-ID</td>
    <xsl:if test="count(LOGINID)>0">
     <td><xsl:value-of select="LOGINID"/></td>
     <td/>
    </xsl:if>
    <xsl:if test="count(LOGINID)=0">
     <td/><td/>
    </xsl:if>     
    
    <td align = "right">MSB</td>
    <xsl:for-each select="KOPF/ZDE">
    <xsl:variable name="varSTELLEpos"><xsl:value-of select="position()"/></xsl:variable>
     <xsl:for-each select="ZDBYTE">
      <td  align = "center">
       <xsl:if test="$varSTELLEpos mod 2 = 1"><xsl:attribute name="bgcolor">#FFEEEE</xsl:attribute></xsl:if>
       <xsl:if test="$varSTELLEpos mod 2!= 1"><xsl:attribute name="bgcolor">#FFFFFF</xsl:attribute></xsl:if>
       <xsl:value-of select="ZMSB"/>
      </td>
     </xsl:for-each>
    </xsl:for-each>
   </tr>

   <!-- 3. Zeile -->
   <tr>
    <xsl:attribute name="bgcolor">#EEEEEE</xsl:attribute>
    <td>HSC</td>
    <xsl:if test="count(HSC)>0">
     <td>
      <xsl:for-each select="HSC"> 
       <xsl:if test="last()=position()">
        <xsl:value-of select="."/>
       </xsl:if>
       <xsl:if test="last()!=position()">
        <xsl:value-of select="concat(., ',')"/>
       </xsl:if>
      </xsl:for-each>
     </td>
     <td/>
    </xsl:if>
    <xsl:if test="count(HSC)=0">
     <td/><td/>
    </xsl:if>
    
    <td align = "right">LSB</td>
    <xsl:for-each select="KOPF/ZDE">
     <xsl:variable name="varSTELLEpos"><xsl:value-of select="position()"/></xsl:variable>
     <xsl:for-each select="ZDBYTE">
      <td align = "center">
       <xsl:if test="$varSTELLEpos mod 2 = 1"><xsl:attribute name="bgcolor">#FFEEEE</xsl:attribute></xsl:if>
       <xsl:if test="$varSTELLEpos mod 2!= 1"><xsl:attribute name="bgcolor">#FFFFFF</xsl:attribute></xsl:if>
       <xsl:value-of select="ZLSB"/>
      </td>
     </xsl:for-each>
    </xsl:for-each>
   </tr>

  <tr>
   <td colspan = "2"  align = "center">PR - FAMILIE</td><td colspan="2" align = "center">PR - NUMMER</td>
   <xsl:for-each select="KOPF/ZDE">
    <xsl:variable name="varSTELLEpos"><xsl:value-of select="position()"/></xsl:variable>
    <xsl:for-each select="ZDBYTE">
     <td style="writing-mode:tb-rl">
      <xsl:if test="$varSTELLEpos mod 2 = 1"><xsl:attribute name="bgcolor">#FFEEEE</xsl:attribute></xsl:if>
      <xsl:value-of select="ZBEZ"/></td>
    </xsl:for-each>
   </xsl:for-each>
  </tr>
  <xsl:for-each select="TAB/FAM">
   <xsl:variable name="varPRNFAMILIENUMMER"><xsl:value-of select="FAMNR"/></xsl:variable>
   <xsl:variable name="varPRNFAMILIENBEZ"><xsl:value-of select="FAMBEZ"/></xsl:variable>
   <xsl:variable name="varFAMpos"><xsl:value-of select="position()"/></xsl:variable>
   <xsl:for-each select="TEGUE">
    <tr>
     <xsl:if test="$varFAMpos mod 2 = 1"><xsl:attribute name="bgcolor">#EEFFEE</xsl:attribute></xsl:if>
     
      <xsl:if test="position() = 1">
       <td>
        <xsl:attribute name="rowspan"><xsl:value-of select="count(../TEGUE)"/></xsl:attribute>
        <xsl:value-of select="../FAMNR"/>
       </td>
       <td>
        <xsl:attribute name="rowspan"><xsl:value-of select="count(../TEGUE)"/></xsl:attribute>
        <xsl:value-of select="../FAMBEZ"/>
       </td>
      </xsl:if>
      <td>
       <xsl:value-of select="PRNR"/>
      </td>
      <td>
       <xsl:value-of select="PRBEZ"/>
      </td>
      <xsl:variable name="varPRNNUMMER"><xsl:value-of select="PRNR"/></xsl:variable>

      <!-- Tabellenfeld fuellen-->
      <!-- Alle Positionen der Spaltenkoepfe durchlaufen-->
      <xsl:for-each select="../../../KOPF/ZDE">
       <xsl:variable name="varSTELLEpos"><xsl:value-of select="position()"/></xsl:variable>
       <xsl:variable name="varStelle"><xsl:value-of select="ZDSTELLE"/></xsl:variable>
       <xsl:for-each select="ZDBYTE">
        <xsl:variable name="varLSB"><xsl:value-of select="ZLSB"/></xsl:variable>

        <!-- Alle PRNVERKNUEPFUNGEN der PRNUMMER durchlaufen -->
        <xsl:variable name="varVARNAME"><xsl:value-of  select="../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER and FAMBEZ=$varPRNFAMILIENBEZ]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/VARNAME"/></xsl:variable>
        <xsl:variable name="varWERT"><xsl:value-of  select="../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER and FAMBEZ=$varPRNFAMILIENBEZ]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/WERT"/></xsl:variable>
        <xsl:variable name="varDATEINAME"><xsl:value-of  select="../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER and FAMBEZ=$varPRNFAMILIENBEZ]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/DATEINAME"/></xsl:variable>
        <xsl:variable name="varFEHLER"><xsl:value-of  select="../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER and FAMBEZ=$varPRNFAMILIENBEZ]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/FEHLER"/></xsl:variable>
        <xsl:variable name="varUNGUELTIG"><xsl:value-of  select="../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER and FAMBEZ=$varPRNFAMILIENBEZ]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/UNGUELTIG"/></xsl:variable>
        <xsl:variable name="varUEBERSPRINGEN"><xsl:value-of  select="../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER and FAMBEZ=$varPRNFAMILIENBEZ]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/UEBERSPRINGEN"/></xsl:variable>
        <xsl:variable name="varDATEN-NAME"><xsl:value-of  select="../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER and FAMBEZ=$varPRNFAMILIENBEZ]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/DATEN-NAME"/></xsl:variable>
        <xsl:choose>
        <xsl:when test="$varDATEINAME!=''">
    <td align = "center"><xsl:apply-templates select="../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/DATEINAME"/></td>
        </xsl:when>
        <xsl:when test="$varDATEN-NAME!=''">
    <td align = "center"><xsl:apply-templates select="../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/DATEN-NAME"/></td>
        </xsl:when>
        <xsl:when test="$varVARNAME!=''">
    <td align = "center"><xsl:apply-templates select="../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/VARNAME"/></td>
        </xsl:when>
        <xsl:when test="$varFEHLER!=''">
    <td align = "center"><xsl:apply-templates select="../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/FEHLER"/></td>
        </xsl:when>
        <xsl:when test="count(../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/FEHLER)>0">
    <td align = "center"><xsl:attribute name="bgcolor">#FF0000</xsl:attribute>ERROR</td>
        </xsl:when>
        <xsl:when test="$varUNGUELTIG!=''">
    <td align = "center"><xsl:apply-templates select="../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/UNGUELTIG"/></td>
        </xsl:when>
	<xsl:when test="count(../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/UNGUELTIG)>0">
    <td align = "center"><xsl:attribute name="bgcolor">#F0F000</xsl:attribute>N/A</td>
        </xsl:when>
        <xsl:when test="$varUEBERSPRINGEN!=''">
    <td align = "center"><xsl:apply-templates select="../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/UEBERSPRINGEN"/></td>
        </xsl:when>
        <xsl:when test="count(../../../TAB/FAM[FAMNR=$varPRNFAMILIENUMMER]/TEGUE[PRNR=$varPRNNUMMER]/KNOTEN[STELLE=$varStelle and LSB=$varLSB]/UEBERSPRINGEN)>0">
    <td align = "center"><xsl:attribute name="bgcolor">#F0F000</xsl:attribute>N/A</td>
        </xsl:when>
        <xsl:when test="$varWERT!=''">
          <td align = "center">
           <xsl:choose>
            <xsl:when test="$varFAMpos mod 2 = 1 and $varSTELLEpos mod 2 = 1"><xsl:attribute name="bgcolor">#F8F8EE</xsl:attribute></xsl:when>
            <xsl:when test="$varFAMpos mod 2 = 0 and $varSTELLEpos mod 2 = 1"><xsl:attribute name="bgcolor">#FFEEEE</xsl:attribute></xsl:when>
           </xsl:choose>
           <xsl:value-of  select="$varWERT"/>
          </td>
         </xsl:when>
        <xsl:otherwise>
         <td align = "center" >
          <xsl:choose>
           <xsl:when test="$varFAMpos mod 2 = 1 and $varSTELLEpos mod 2 = 1"><xsl:attribute name="bgcolor">#F8F8EE</xsl:attribute></xsl:when>
           <xsl:when test="$varFAMpos mod 2 = 0 and $varSTELLEpos mod 2 = 1"><xsl:attribute name="bgcolor">#FFEEEE</xsl:attribute></xsl:when>
          </xsl:choose>
          .
         </td>
        </xsl:otherwise>
       </xsl:choose>
      </xsl:for-each>
     </xsl:for-each>
     <!-- ENDE Tabellenfeld fuellen-->

    </tr>
   </xsl:for-each>
   <p/>
  </xsl:for-each>
 </table>
 <hr />
</xsl:template>

</xsl:stylesheet>