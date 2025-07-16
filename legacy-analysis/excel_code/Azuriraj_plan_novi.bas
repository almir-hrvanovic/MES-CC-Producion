Attribute VB_Name = "Azuriraj_plan_novi"
Sub Azuriraj222()

'ST - Start Time Date
'STT - Start Time Time
'OT - Order Time
'CET - Calculated End Time
'STZ - Start Time Zone
'CETZ - Calculated End Time Zone
'ZBT - Zone Break Time
'BET - Break End Time
'BT - Break Time
'BRN - Broj Radnih Naloga

Dim ST As Date
Dim STT As Date
Dim BTT As Date
Dim CET As Date
Dim OT As Date
Dim ZT1 As Date
Dim ZT2 As Date
Dim ZT3 As Date
Dim ZT4 As Date
Dim DELTA As Date
Dim WSST As Date
Dim WSET As Date
Dim ST1 As Date
Dim ST2 As Date
Dim ST3 As Date
Dim ST4 As Date

Dim T1 As Date
Dim T2 As Date
Dim T3 As Date
Dim TIME As Date

'Dim btDate As Date
'Dim stDate As Date

                                                                                                    Dim CurrentProgress As Double
                                                                                                    Dim ProgressPercentage As Double
                                                                                                    Dim BarWidth As Long

TIME = Now()

With Application
    .ScreenUpdating = False
    .Calculation = xlManual
    .DisplayStatusBar = False
End With

ST1 = "00:00:00"
ST2 = "07:00:00"
ST3 = "15:00:00"
ST4 = "23:00:00"
ST5 = "24:00:00"

ZT1 = "00:00:00"
ZT2 = "02:00:00"
ZT3 = "10:00:00"
ZT4 = "18:00:00"
ZT5 = "24:00:00"

BD = Sheets("PRINT").Range("O2").Value
ST = Sheets("PRINT").Range("R3").Value
STT = TimeSerial(Hour(ST), Minute(ST), Second(ST))
stDate = CDbl(Int(ST))

Set OPSEG = Sheets("KALENDAR MASINA").Range("A:E")

' S1       ST2 = "07:00:00" ST3 = "15:00:00"
If (STT >= ST2) And (STT < ST3) Then
    STWS = Application.WorksheetFunction.VLookup(stDate, OPSEG, 3, False)
' S2           ST3 = "15:00:00" ST4 = "23:00:00"
ElseIf (STT >= ST3) And (STT < ST4) Then
    STWS = Application.WorksheetFunction.VLookup(stDate, OPSEG, 4, False)
' S3         'ST4 = "23:00:00" ST5 = "24:00:00"
ElseIf (STT >= ST4) And (STT <= ST5) Then
    STWS = Application.WorksheetFunction.VLookup(stDate, OPSEG, 5, False)
' S3           ST1 = "00:00:00" ST2 = "07:00:00"
ElseIf (STT >= ST1) And (STT < ST2) Then
    STWS = Application.WorksheetFunction.VLookup(stDate - 1, OPSEG, 5, False)
End If

If STWS = "r" Then
     
' >>>>>> CISCENJE SHEET NOVO
                                                                                                 Call InitProgressBar
    Sheets("NOVO").Range("A1").CurrentRegion.ClearContents
    With Sheets("PRINT").Range("A5").CurrentRegion.Offset(4).Interior
        .Pattern = xlNone
        .TintAndShade = 0
        .PatternTintAndShade = 0
    End With
    With Sheets("PRINT").Range("A5").CurrentRegion.Offset(4).Font
        .ColorIndex = xlAutomatic
        .TintAndShade = 0
        .Underline = xlUnderlineStyleNone
    End With
    Sheets("PRINT").Range("A5").CurrentRegion.Offset(4).ClearContents
    
    
' >>>>>> POPUNI SHEET NOVO

Sheets("QUERY").Select

        If Sheets("PRINT").Range("K1").Value = True Then
        
            Sheets("PRINT").Range("P4").Value = "Datum PZ"
                                                                            '21 - U
    ActiveSheet.ListObjects("PlanMasine").Range.AutoFilter Field:=17, Criteria1 _
        :="0"
    ActiveSheet.ListObjects("PlanMasine").Range.AutoFilter Field:=19, Criteria1 _
        :="<" & BD, Operator:=xlAnd

        Else
        
            Sheets("PRINT").Range("P4").Value = "Datum PS"
                                                                            '21 - U
    ActiveSheet.ListObjects("PlanMasine").Range.AutoFilter Field:=17, Criteria1 _
        :="0"
    
    
                If Sheets("PRINT").Range("K3").Value = True Then
    
                    ActiveSheet.ListObjects("PlanMasine").Range.AutoFilter Field:=19, Criteria1 _
                        :="<" & BD, Operator:=xlAnd
                        
                End If
          
        End If
        
        Range("PlanMasine[[#Headers],[KPL]:[Datum SAS]]").Select
            Range(Selection, Selection.End(xlDown)).Select
            Selection.Copy
    
        Sheets("NOVO").Select
            Range("A1").Select
            Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
             :=False, Transpose:=False
            Columns("A:N").EntireColumn.AutoFit
            
            Sheets("QUERY").Select
            Columns("O:O").Select
            Selection.Copy
            Sheets("NOVO").Select
            Columns("E:E").Select
            ActiveSheet.Paste
            
            Sheets("QUERY").Select
            Columns("P:P").Select
            Selection.Copy
            Sheets("NOVO").Select
            Columns("O:O").Select
            ActiveSheet.Paste
            
            Sheets("QUERY").Select
            Columns("R:R").Select
            Selection.Copy
            Sheets("NOVO").Select
            Columns("P:P").Select
            ActiveSheet.Paste
            
            
    
        If Sheets("PRINT").Range("K1").Value = True Then
            
            Sheets("QUERY").Select
            Columns("W:W").Select   ' POMJEREN DATUM
            Selection.Copy
            Sheets("NOVO").Select
            Columns("N:N").Select
            ActiveSheet.Paste
            
        End If
      
            Columns("A:P").Select
            
    ActiveWorkbook.Worksheets("NOVO").Sort.SortFields.Clear
    ActiveWorkbook.Worksheets("NOVO").Sort.SortFields.Add Key:=Range( _
        "P2:P1048576"), SortOn:=xlSortOnValues, Order:=xlAscending, DataOption:= _
        xlSortNormal
    ActiveWorkbook.Worksheets("NOVO").Sort.SortFields.Add Key:=Range( _
        "N2:N1048576"), SortOn:=xlSortOnValues, Order:=xlAscending, DataOption:= _
        xlSortNormal
        
    With ActiveWorkbook.Worksheets("NOVO").Sort
        .SetRange Columns("A:P")
        .Header = xlYes
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With

    Sheets("QUERY").ShowAllData

'T1

T1 = Now() - TIME
Sheets("TIME").Range("A1").Value = T1
TIME = Now()
    
    Sheets("NOVO").Range("A2").Select
    Y = Application.WorksheetFunction.Count(Sheets("NOVO").Range("A2", Range("A2").End(xlDown)))
    
    Z = 5
    ET = Sheets("PRINT").Range("R3").Value + 7
    OT = Sheets("NOVO").Range("M2").Value
        

' --------------------------------------------------------------------------------------------------POPUNJAVANJE


For R = 1 To Y
                                                                                                            CurrentProgress = R / Y
                                                                                                            BarWidth = Progress.Border.Width * CurrentProgress
                                                                                                            ProgressPercentage = Round(CurrentProgress * 100, 0)
        
                                                                                                            Progress.Bar.Width = BarWidth
                                                                                                            Progress.Text.Caption = ProgressPercentage & "%"
                                                                                                            DoEvents
                                                                                                            
                                                                                                            'If ProgressPercentage = 11 Then Stop

Ponovo:

    ST = Sheets("PRINT").Range("R" & Z - 1).Value
    STT = TimeSerial(Hour(ST), Minute(ST), Second(ST))
    CET = ST + OT
    
' IZLAZAK IZ PETLJE
    
       ' If ST > ET And Sheets("PRINT").Range("K3").Value = True Then Exit Do
        
      
' ODREÐIVANJE TERMINA PAUZE

    'BT       ZT4 = "18:00:00" ZT5 = "24:00:00"
    If (STT > ZT4) And (STT <= ZT5) Then
        BT = Int(ST) + 1 + ZT2
    'BT            ZT1 = "00:00:00" ZT2 = "02:00:00"
    ElseIf (STT >= ZT1) And (STT <= ZT2) Then
        BT = Int(ST) + ZT2
    'BT           ZT2 = "02:00:00" ZT3 = "10:00:00"
    ElseIf (STT > ZT2) And (STT <= ZT3) Then
        BT = Int(ST) + ZT3
    'BT           ZT3 = "10:00:00" ZT4 = "18:00:00"
    ElseIf (STT > ZT3) And (STT <= ZT4) Then
        BT = Int(ST) + ZT4
    End If
    
    ' S1       ST2 = "07:00:00" ST3 = "15:00:00"
    If (STT >= ST2) And (STT < ST3) Then
        WSST = Int(ST) + ST2
        WSET = Int(ST) + ST3
    ' S2           ST3 = "15:00:00" ST4 = "23:00:00"
    ElseIf (STT >= ST3) And (STT < ST4) Then
        WSST = Int(ST) + ST3
        WSET = Int(ST) + ST4
    ' S3         'ST4 = "23:00:00" ST5 = "24:00:00"
    ElseIf (STT >= ST4) And (STT <= ST5) Then
        WSST = Int(ST) + ST4
        WSET = Int(ST) + 1 + ST2
    ' S3           ST1 = "00:00:00" ST2 = "07:00:00"
    ElseIf (STT >= ST1) And (STT < ST2) Then
        WSST = Int(ST) - 1 + ST4
        WSET = Int(ST) + ST2
    End If
   
' ODREÐIVANJE RADNE SMJENE NA OSNOVU PAUZE
      
        BTT = TimeSerial(Hour(BT), Minute(BT), Second(BT))
        btDate = CDbl(Int(BT))
        STT = TimeSerial(Hour(ST), Minute(ST), Second(ST))
        stDate = CDbl(Int(ST))

        ' S1       ST2 = "07:00:00" ST3 = "15:00:00"
            If (BTT >= ST2) And (BTT < ST3) Then
                BTWS = Application.WorksheetFunction.VLookup(btDate, OPSEG, 3, False)
        ' S2           ST3 = "15:00:00" ST4 = "23:00:00"
            ElseIf (BTT >= ST3) And (BTT < ST4) Then
                BTWS = Application.WorksheetFunction.VLookup(btDate, OPSEG, 4, False)
        ' S3         'ST4 = "23:00:00" ST5 = "24:00:00"
            ElseIf (BTT >= ST4) And (BTT <= ST5) Then
                BTWS = Application.WorksheetFunction.VLookup(btDate, OPSEG, 5, False)
        ' S3           ST1 = "00:00:00" ST2 = "07:00:00"
            ElseIf (BTT >= ST1) And (BTT < ST2) Then
                BTWS = Application.WorksheetFunction.VLookup(btDate - 1, OPSEG, 5, False)
            End If
            
        ' S1       ST2 = "07:00:00" ST3 = "15:00:00"
            If (STT >= ST2) And (STT < ST3) Then
                STWS = Application.WorksheetFunction.VLookup(stDate, OPSEG, 3, False)
        ' S2           ST3 = "15:00:00" ST4 = "23:00:00"
            ElseIf (STT >= ST3) And (STT < ST4) Then
                STWS = Application.WorksheetFunction.VLookup(stDate, OPSEG, 4, False)
        ' S3         'ST4 = "23:00:00" ST5 = "24:00:00"
            ElseIf (STT >= ST4) And (STT <= ST5) Then
                STWS = Application.WorksheetFunction.VLookup(stDate, OPSEG, 5, False)
        ' S3           ST1 = "00:00:00" ST2 = "07:00:00"
            ElseIf (STT >= ST1) And (STT < ST2) Then
                STWS = Application.WorksheetFunction.VLookup(stDate - 1, OPSEG, 5, False)
            End If
    
' <<<<<<<  >>>>>>> UPISIVANJE NOVOG REDA U ZAVISNOSTI OD CET, BT, BTWS
    
    
'CASE 1 - Unutar radne smjene
    
    If (STWS = "r") And (CET <= BT) And (CET <= WSET) Then
    
        Sheets("NOVO").Range(Cells(R + 1, 1), Cells(R + 1, 14)).Copy Sheets("PRINT").Range("C" & Z)
        Sheets("PRINT").Range("O" & Z) = OT
        Sheets("PRINT").Range("A" & Z).FormulaR1C1 = "=INDEX(QUERY!C[7],MATCH(PRINT!RC[4],QUERY!C[2],0))"
        Sheets("PRINT").Range("R" & Z).FormulaR1C1 = "=R[-1]C+RC[-3]"
        Sheets("PRINT").Range("S" & Z).FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
        Sheets("PRINT").Range("G" & Z).FormulaR1C1 = "=HOUR(RC[8])*60+MINUTE(RC[8])"
        
        OT = Sheets("NOVO").Range("M" & R + 2).Value
        Z = Z + 1
            
'CASE 2 - Ubaci pauzu unutar smjene
    
    ElseIf (STWS = "r") And (CET > BT) And (CET <= WSET) Then
       
            Sheets("NOVO").Range(Cells(R + 1, 1), Cells(R + 1, 14)).Copy Sheets("PRINT").Range("C" & Z)
            Sheets("PRINT").Range("O" & Z) = BT - ST   ' rekalkulacija trajanja
            Sheets("PRINT").Range("A" & Z).FormulaR1C1 = "=INDEX(QUERY!C[7],MATCH(PRINT!RC[4],QUERY!C[2],0))"   ' pretraga cekiranja
            Sheets("PRINT").Range("R" & Z).FormulaR1C1 = "=R[-1]C+RC[-3]"   ' kalkulacija završetka
            Sheets("PRINT").Range("S" & Z).FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"  ' kalkulacija vremena završetka
            Sheets("PRINT").Range("G" & Z).FormulaR1C1 = "=HOUR(RC[8])*60+MINUTE(RC[8])"  ' konverzija norme u minute
            
            ' UBACIVANJE PAUZE
                Z = Z + 1
                Sheets("PRINT").Range("N" & Z) = "PAUZA"
                Sheets("PRINT").Range("O" & Z) = "00:30:00"
                Sheets("PRINT").Range("P" & Z) = Sheets("PRINT").Range("P" & Z - 1).Value
                Sheets("PRINT").Range("R" & Z).FormulaR1C1 = "=R[-1]C+RC[-3]"
                Sheets("PRINT").Range("S" & Z).FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
            
            TD = OT - (BT - ST)
            OT = TD
            Z = Z + 1
            
            GoTo Ponovo
                
'CASE 3 - Naredna smjena neradna
     
     ElseIf (STWS = "r") And (BTWS = "n") And (CET > WSET) Then
       
        Sheets("NOVO").Range(Cells(R + 1, 1), Cells(R + 1, 14)).Copy Sheets("PRINT").Range("C" & Z)
            Sheets("PRINT").Range("O" & Z) = WSET - ST   ' rekalkulacija trajanja
            Sheets("PRINT").Range("A" & Z).FormulaR1C1 = "=INDEX(QUERY!C[7],MATCH(PRINT!RC[4],QUERY!C[2],0))"   ' pretraga cekiranja
            Sheets("PRINT").Range("R" & Z).FormulaR1C1 = "=R[-1]C+RC[-3]"   ' kalkulacija završetka
            Sheets("PRINT").Range("S" & Z).FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"  ' kalkulacija vremena završetka
            Sheets("PRINT").Range("G" & Z).FormulaR1C1 = "=HOUR(RC[8])*60+MINUTE(RC[8])"  ' konverzija norme u minute
            
            ' UBACIVANJE NERADNO
                Z = Z + 1
                Sheets("PRINT").Range("N" & Z) = "NERADNO"
                Sheets("PRINT").Range("O" & Z) = "08:00:00"
                Sheets("PRINT").Range("P" & Z) = Sheets("PRINT").Range("P" & Z - 1).Value
                Sheets("PRINT").Range("R" & Z).FormulaR1C1 = "=R[-1]C+RC[-3]"
                Sheets("PRINT").Range("S" & Z).FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
            
            TD = OT - (WSET - ST)
            OT = TD
            Z = Z + 1
            
            GoTo Ponovo
               
'CASE 4 - Naredna smjena radna CET > WSET & CET < BT
    
        ElseIf (STWS = "r") And (BTWS = "r") And (CET > WSET) And (CET <= BT) Then
       
        Sheets("NOVO").Range(Cells(R + 1, 1), Cells(R + 1, 14)).Copy Sheets("PRINT").Range("C" & Z)
        Sheets("PRINT").Range("O" & Z) = OT
        Sheets("PRINT").Range("A" & Z).FormulaR1C1 = "=INDEX(QUERY!C[7],MATCH(PRINT!RC[4],QUERY!C[2],0))"
        Sheets("PRINT").Range("R" & Z).FormulaR1C1 = "=R[-1]C+RC[-3]"
        Sheets("PRINT").Range("S" & Z).FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
        Sheets("PRINT").Range("G" & Z).FormulaR1C1 = "=HOUR(RC[8])*60+MINUTE(RC[8])"
        
        OT = Sheets("NOVO").Range("M" & R + 2).Value
        Z = Z + 1
               
'CASE 5 - Naredna smjena radna ali CET > WSET & CET > BT
                  
    ElseIf (STWS = "r") And (BTWS = "r") And (CET > BT) Then
       
        Sheets("NOVO").Range(Cells(R + 1, 1), Cells(R + 1, 14)).Copy Sheets("PRINT").Range("C" & Z)
            Sheets("PRINT").Range("O" & Z) = BT - ST   ' rekalkulacija trajanja
            Sheets("PRINT").Range("A" & Z).FormulaR1C1 = "=INDEX(QUERY!C[7],MATCH(PRINT!RC[4],QUERY!C[2],0))"   ' pretraga cekiranja
            Sheets("PRINT").Range("R" & Z).FormulaR1C1 = "=R[-1]C+RC[-3]"   ' kalkulacija završetka
            Sheets("PRINT").Range("S" & Z).FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"  ' kalkulacija vremena završetka
            Sheets("PRINT").Range("G" & Z).FormulaR1C1 = "=HOUR(RC[8])*60+MINUTE(RC[8])"  ' konverzija norme u minute
            
            ' UBACIVANJE PAUZE
                Z = Z + 1
                Sheets("PRINT").Range("N" & Z) = "PAUZA"
                Sheets("PRINT").Range("O" & Z) = "00:30:00"
                Sheets("PRINT").Range("P" & Z) = Sheets("PRINT").Range("P" & Z - 1).Value
                Sheets("PRINT").Range("R" & Z).FormulaR1C1 = "=R[-1]C+RC[-3]"
                Sheets("PRINT").Range("S" & Z).FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
            
            TD = OT - (BT - ST)
            OT = TD
            Z = Z + 1
            
            GoTo Ponovo
               
'CASE 6 - Ubaci neradnu smjenu
               
    ElseIf (STWS = "n") And (BTWS = "n") Then
                 
                Sheets("PRINT").Range("N" & Z) = "NERADNO"
                Sheets("PRINT").Range("O" & Z) = "08:00:00"
                Sheets("PRINT").Range("P" & Z) = Sheets("PRINT").Range("P" & Z - 1).Value
                Sheets("PRINT").Range("R" & Z).FormulaR1C1 = "=R[-1]C+RC[-3]"
                Sheets("PRINT").Range("S" & Z).FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
                Z = Z + 1
                GoTo Ponovo
    End If
    
Next R
    
'T2
T2 = Now() - TIME
Sheets("TIME").Range("A2").Value = T2
TIME = Now()
                                                                                                                   Unload Progress

    Sheets("PRINT").Select
    
    Range("T5").FormulaR1C1 = "=RC[-4]-(RC[-2]-RC[-1])"
    Range("T5").AutoFill Destination:=Range("T5", Cells(Z - 1, 20)), Type:=xlFillValues
    
    Range("Q5").FormulaR1C1 = "=R[-1]C[1]"
    Range("Q5").AutoFill Destination:=Range("Q5", Cells(Z - 1, 17)), Type:=xlFillValues
    
    Range("U5").FormulaR1C1 = "=IFERROR(INDEX(NOVO!C[-6],MATCH(PRINT!RC[-16],NOVO!C[-18],0)),"""")"
    Range("U5").AutoFill Destination:=Range("U5", Cells(Z, 21)), Type:=xlFillValues
    
    
    
Application.Calculation = xlAutomatic
    
Else

MsgBox "Neradna smjena, unesite novi datum i vrijeme ili podesite radne smjene!"
    
End If

'T3
T3 = Now() - TIME
Sheets("TIME").Range("A3").Value = T3

Range("A5", Cells(Z, 20)).Copy
Sheets("PRINT").Range("A5").PasteSpecial xlPasteValues

Range("A5:U5").Copy

    Range("A6", Cells(Z - 1, 21)).PasteSpecial Paste:=xlPasteFormats, Operation:=xlNone, _
        SkipBlanks:=False, Transpose:=False
    Application.CutCopyMode = False
   
Range("A1").Select

Sheets("NOVO").Select
        Application.CutCopyMode = False
        Range("Q2").FormulaR1C1 = "=RC[-16]&""-""&RC[-14]"
        X = Application.WorksheetFunction.Count(Sheets("NOVO").Range("A1", Range("A1").End(xlDown)))
        Range("Q2").AutoFill Destination:=Range("Q2", Cells(X + 1, 17)), Type:=xlFillValues
        Range("Q2").Select
        Range(Selection, Selection.End(xlDown)).Select
        Selection.Copy
        Range("Q2").Select
        Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False
   
Sheets("PRINT").Select

Application.DisplayStatusBar = True



End Sub

Sub InitProgressBar()

With Progress
    .Bar.Width = 0
    .Text.Caption = "0% Završeno!"
    .Show vbModeless
End With

End Sub

Sub Provjera_smjene()

Dim ST1 As Date
Dim ST2 As Date
Dim ST3 As Date
Dim ST4 As Date

ST1 = "00:00:00"
ST2 = "07:00:00"
ST3 = "15:00:00"
ST4 = "23:00:00"
ST5 = "24:00:00"

ST = Selection.Value
STT = TimeSerial(Hour(ST), Minute(ST), Second(ST))
stDate = CDbl(Int(ST))

Sheets("KALENDAR MASINA").Activate

Set OPSEG = Range("A:E")

' S1       ST2 = "07:00:00" ST3 = "15:00:00"
If (STT >= ST2) And (STT < ST3) Then
    STWS = Application.WorksheetFunction.VLookup(stDate, OPSEG, 3, False)
' S2           ST3 = "15:00:00" ST4 = "23:00:00"
ElseIf (STT >= ST3) And (STT < ST4) Then
    STWS = Application.WorksheetFunction.VLookup(stDate, OPSEG, 4, False)
' S3         'ST4 = "23:00:00" ST5 = "24:00:00"
ElseIf (STT >= ST4) And (STT <= ST5) Then
    STWS = Application.WorksheetFunction.VLookup(stDate, OPSEG, 5, False)
' S3           ST1 = "00:00:00" ST2 = "07:00:00"
ElseIf (STT >= ST1) And (STT < ST2) Then
    STWS = Application.WorksheetFunction.VLookup(stDate - 1, OPSEG, 5, False)
End If

End Sub


