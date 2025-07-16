Attribute VB_Name = "Azuriraj_plan_stari"
Sub Azuriraj_plan()

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

Dim CurrentProgress As Double
Dim ProgressPercentage As Double
Dim BarWidth As Long

Application.ScreenUpdating = False
Application.Calculation = xlManual

ST1 = "00:00:00"
ST2 = "07:00:00"
ST3 = "15:00:00"
ST4 = "23:00:00"
ST5 = "24:00:00"

DELTA = "03:00:00"

Sheets("PLAN").Select
Range("R3").Select

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

If STWS = "r" Then
     
' >>>>>> CISCENJE SHEET NOVO I PLAN

Call InitProgressBar

    Sheets("NOVO").Select
        Range("A1:O2000").Select
        Selection.ClearContents
    Sheets("PLAN").Select
        Range("A5:T2000").Select
        Selection.ClearContents
    
    With Selection.Interior
        .Pattern = xlNone
        .TintAndShade = 0
        .PatternTintAndShade = 0
    End With
    With Selection.Font
        .ColorIndex = xlAutomatic
        .TintAndShade = 0
    End With
    
' >>>>>> POPUNI SHEET NOVO

Sheets("QUERY").Select
                                                                            '14 - N
        ActiveSheet.ListObjects("Table_Query_from_Mladen4").Range.AutoFilter Field:= _
            14, Criteria1:="<>Nema datum!"
                                                                            '19 - S
        ActiveSheet.ListObjects("Table_Query_from_Mladen4").Range.AutoFilter Field:= _
            19, Criteria1:="FALSE"
                                                                            '20 - T
        ActiveSheet.ListObjects("Table_Query_from_Mladen4").Range.AutoFilter Field:= _
            20, Criteria1:="FALSE"
                                                                            '21 - U
        ActiveSheet.ListObjects("Table_Query_from_Mladen4").Range.AutoFilter Field:= _
            21, Criteria1:="0"
        
        Range("Table_Query_from_Mladen4[[#Headers],[KPL]:[Datum SAS]]").Select
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
            Columns("V:V").Select
            Selection.Copy
            Sheets("NOVO").Select
            Columns("O:O").Select
            ActiveSheet.Paste
    
            Columns("A:O").Select
            
    ActiveWorkbook.Worksheets("NOVO").Sort.SortFields.Clear
    ActiveWorkbook.Worksheets("NOVO").Sort.SortFields.Add Key:=Range( _
        "O2:O1048576"), SortOn:=xlSortOnValues, Order:=xlDescending, DataOption:= _
        xlSortNormal
    ActiveWorkbook.Worksheets("NOVO").Sort.SortFields.Add Key:=Range( _
        "N2:N1048576"), SortOn:=xlSortOnValues, Order:=xlAscending, DataOption:= _
        xlSortNormal
        
    With ActiveWorkbook.Worksheets("NOVO").Sort
        .SetRange Columns("A:O")
        .Header = xlYes
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With

    Sheets("QUERY").Select
        ActiveSheet.ShowAllData


' >>>>>> POPUNJAVANJE PLANA
    
    
    Sheets("NOVO").Select
        Range("A2").Select
        Range(Selection, Selection.End(xlDown)).Select
        Y = Selection.Count
        
        Range("A2").Select
        
Do Until ActiveCell.Value = ""
      
      
    CurrentProgress = X / Y
    BarWidth = Progress.Border.Width * CurrentProgress
    ProgressPercentage = Round(CurrentProgress * 100, 0)
        
    Progress.Bar.Width = BarWidth
    Progress.Text.Caption = ProgressPercentage & "%"
    DoEvents


    OT = ActiveCell.Offset(0, 12).Value
    
    Sheets("PLAN").Select
        Range("R3").Select
        Selection.End(xlDown).Select
   
      
    ST = Selection.Value
        STT = TimeSerial(Hour(ST), Minute(ST), Second(ST))
    CET = ST + OT
      
      
' ODREÐIVANJE TERMINA PAUZE

ZT1 = "00:00:00"
ZT2 = "02:00:00"
ZT3 = "10:00:00"
ZT4 = "18:00:00"
ZT5 = "24:00:00"

ST1 = "00:00:00"
ST2 = "07:00:00"
ST3 = "15:00:00"
ST4 = "23:00:00"
ST5 = "24:00:00"



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
            
        Sheets("KALENDAR MASINA").Activate
        Set OPSEG = Range("A:E")

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
    
        Sheets("NOVO").Select
            Range(Selection, Selection.Offset(0, 13)).Select
            Selection.Copy
    
        Sheets("PLAN").Select
        
            Range("C" & Rows.Count).End(xlUp).Offset(1, 0).Select
            
            Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
              :=False, Transpose:=False
            
            Range("A" & Rows.Count).End(xlUp).Offset(1, 0).Select
            ActiveCell.FormulaR1C1 = "=INDEX(QUERY!C[7],MATCH(PLAN!RC[4],QUERY!C[2],0))"
            Range("R" & Rows.Count).End(xlUp).Offset(1, 0).Select
            ActiveCell.FormulaR1C1 = "=R[-1]C+RC[-3]"
            Range("S" & Rows.Count).End(xlUp).Offset(1, 0).Select
            ActiveCell.FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
            
            Sheets("NOVO").Select
            ActiveCell.Offset(1, 0).Select
            X = ActiveCell.Row - 1
            
    'CASE 2 - Ubaci pauzu unutar smjene
    
    ElseIf (STWS = "r") And (CET > BT) And (CET <= WSET) Then
       
        Sheets("NOVO").Select
            Range(Selection, Selection.Offset(0, 13)).Select
            Selection.Copy
    
        Sheets("PLAN").Select
        
            Range("C" & Rows.Count).End(xlUp).Offset(1, 0).Select
            
            Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
              :=False, Transpose:=False
              
        Sheets("NOVO").Select
            
            ActiveCell.Offset(1, 0).Select
            ActiveCell.EntireRow.Select
            Selection.Insert Shift:=xlDown, CopyOrigin:=xlFormatFromLeftOrAbove
            ActiveCell.Offset(-1, 0).Select
            Range(Selection, Selection.Offset(0, 13)).Select
            Selection.Copy
            ActiveCell.Offset(1, 0).Select
            Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
              :=False, Transpose:=False
              
        Sheets("PLAN").Select
            
 
            Range("O" & Rows.Count).End(xlUp).Select
                ActiveCell.Value = BT - ST
            Range("A" & Rows.Count).End(xlUp).Offset(1, 0).Select
                ActiveCell.FormulaR1C1 = "=INDEX(QUERY!C[7],MATCH(PLAN!RC[4],QUERY!C[2],0))"
            Range("R" & Rows.Count).End(xlUp).Offset(1, 0).Select
                ActiveCell.FormulaR1C1 = "=R[-1]C+RC[-3]"
            Range("S" & Rows.Count).End(xlUp).Offset(1, 0).Select
                ActiveCell.FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
            Range("G" & Rows.Count).End(xlUp).Select
                ActiveCell.FormulaR1C1 = "=HOUR(RC[8])*60+MINUTE(RC[8])"
                ActiveCell = ActiveCell.Value
                
                    TD = OT - (BT - ST)
                
                Sheets("NOVO").Select
                    ActiveCell.Offset(0, 12).Select
                    ActiveCell = TD
                    ActiveCell.Offset(0, -8).Select
                    ActiveCell = "=HOUR(RC[8])*60+MINUTE(RC[8])"
                                       
                    ActiveCell = ActiveCell.Value
                    ActiveCell.Offset(-1, -4).Select
                    
               ' UBACIVANJE PAUZE
               
                Sheets("KALENDAR MASINA").Select
                    Range("AA1:AP1").Copy
                    Sheets("PLAN").Select
                    
                    Range("A" & Rows.Count).End(xlUp).Offset(1, 0).Select
                        Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
                    :=False, Transpose:=False
                
                    Range("P" & Rows.Count).End(xlUp) = Range("P" & Rows.Count).End(xlUp).Offset(-1, 0).Value
                
                    Range("A" & Rows.Count).End(xlUp).Offset(1, 0) = 0
                                
                    Range("R" & Rows.Count).End(xlUp).Offset(1, 0).Select
                    ActiveCell.FormulaR1C1 = "=R[-1]C+RC[-3]"
            
                    Range("S" & Rows.Count).End(xlUp).Offset(1, 0).Select
                    ActiveCell.FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
                    
                    Call Format_Pauza
                    
            Y = Y + 1
           
            Sheets("NOVO").Select
            ActiveCell.Offset(1, 0).Select
            X = ActiveCell.Row - 1
               
    'CASE 3 - Naredna smjena neradna
     
     ElseIf (STWS = "r") And (BTWS = "n") And (CET > WSET) Then
       
        Sheets("NOVO").Select
            Range(Selection, Selection.Offset(0, 13)).Select
            Selection.Copy
    
        Sheets("PLAN").Select
        
            Range("C" & Rows.Count).End(xlUp).Offset(1, 0).Select
            
            Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
              :=False, Transpose:=False
              
        Sheets("NOVO").Select
            
            ActiveCell.Offset(1, 0).Select
            ActiveCell.EntireRow.Select
            Selection.Insert Shift:=xlDown, CopyOrigin:=xlFormatFromLeftOrAbove
            ActiveCell.Offset(-1, 0).Select
            Range(Selection, Selection.Offset(0, 13)).Select
            Selection.Copy
            ActiveCell.Offset(1, 0).Select
            Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
              :=False, Transpose:=False
              
        Sheets("PLAN").Select
            
            Range("O" & Rows.Count).End(xlUp).Select
                ActiveCell.Value = WSET - ST
            Range("A" & Rows.Count).End(xlUp).Offset(1, 0).Select
                ActiveCell.FormulaR1C1 = "=INDEX(QUERY!C[7],MATCH(PLAN!RC[4],QUERY!C[2],0))"
            Range("R" & Rows.Count).End(xlUp).Offset(1, 0).Select
                ActiveCell.FormulaR1C1 = "=R[-1]C+RC[-3]"
            Range("S" & Rows.Count).End(xlUp).Offset(1, 0).Select
                ActiveCell.FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
            Range("G" & Rows.Count).End(xlUp).Select
                ActiveCell.FormulaR1C1 = "=HOUR(RC[8])*60+MINUTE(RC[8])"
                ActiveCell = ActiveCell.Value
                
                    TD = OT - (WSET - ST)
                
                Sheets("NOVO").Select
                    ActiveCell.Offset(0, 12).Select
                    ActiveCell = TD
                    ActiveCell.Offset(0, -8).Select
                    ActiveCell = "=HOUR(RC[8])*60+MINUTE(RC[8])"
                                       
                    ActiveCell = ActiveCell.Value
                    ActiveCell.Offset(-1, -4).Select
                    
               ' UBACIVANJE NERADNE SMJENE
               
                Sheets("KALENDAR MASINA").Select
                    Range("AA2:AP2").Copy
                    Sheets("PLAN").Select
                    
                    Range("A" & Rows.Count).End(xlUp).Offset(1, 0).Select
                        Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
                    :=False, Transpose:=False
                
                    Range("P" & Rows.Count).End(xlUp) = Range("P" & Rows.Count).End(xlUp).Offset(-1, 0).Value
                
                    Range("A" & Rows.Count).End(xlUp).Offset(1, 0) = 0
                                
                    Range("R" & Rows.Count).End(xlUp).Offset(1, 0).Select
                    ActiveCell.FormulaR1C1 = "=R[-1]C+RC[-3]"
            
                    Range("S" & Rows.Count).End(xlUp).Offset(1, 0).Select
                    ActiveCell.FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
                    
                    Call Format_Neradno
                    
            Y = Y + 1
           
            Sheets("NOVO").Select
            ActiveCell.Offset(1, 0).Select
            X = ActiveCell.Row - 1
               
    'CASE 4 - Naredna smjena radna CET > WSET & CET < BT
    
        ElseIf (STWS = "r") And (BTWS = "r") And (CET > WSET) And (CET <= BT) Then
       
        Sheets("NOVO").Select
            Range(Selection, Selection.Offset(0, 13)).Select
            Selection.Copy
    
        Sheets("PLAN").Select
        
            Range("C" & Rows.Count).End(xlUp).Offset(1, 0).Select
            
            Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
              :=False, Transpose:=False
            
            Range("A" & Rows.Count).End(xlUp).Offset(1, 0).Select
            ActiveCell.FormulaR1C1 = "=INDEX(QUERY!C[7],MATCH(PLAN!RC[4],QUERY!C[2],0))"
            Range("R" & Rows.Count).End(xlUp).Offset(1, 0).Select
            ActiveCell.FormulaR1C1 = "=R[-1]C+RC[-3]"
            Range("S" & Rows.Count).End(xlUp).Offset(1, 0).Select
            ActiveCell.FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
            
            Sheets("NOVO").Select
            ActiveCell.Offset(1, 0).Select
            X = ActiveCell.Row - 1
               
    'CASE 5 - Naredna smjena radna ali CET > WSET & CET > BT
                  
    ElseIf (STWS = "r") And (BTWS = "r") And (CET > BT) Then
       
        Sheets("NOVO").Select
            Range(Selection, Selection.Offset(0, 13)).Select
            Selection.Copy
    
        Sheets("PLAN").Select
        
            Range("C" & Rows.Count).End(xlUp).Offset(1, 0).Select
            
            Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
              :=False, Transpose:=False
              
        Sheets("NOVO").Select
            
            ActiveCell.Offset(1, 0).Select
            ActiveCell.EntireRow.Select
            Selection.Insert Shift:=xlDown, CopyOrigin:=xlFormatFromLeftOrAbove
            ActiveCell.Offset(-1, 0).Select
            Range(Selection, Selection.Offset(0, 13)).Select
            Selection.Copy
            ActiveCell.Offset(1, 0).Select
            Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
              :=False, Transpose:=False
              
        Sheets("PLAN").Select
            
 
            Range("O" & Rows.Count).End(xlUp).Select
                ActiveCell.Value = BT - ST
            Range("A" & Rows.Count).End(xlUp).Offset(1, 0).Select
                ActiveCell.FormulaR1C1 = "=INDEX(QUERY!C[7],MATCH(PLAN!RC[4],QUERY!C[2],0))"
            Range("R" & Rows.Count).End(xlUp).Offset(1, 0).Select
                ActiveCell.FormulaR1C1 = "=R[-1]C+RC[-3]"
            Range("S" & Rows.Count).End(xlUp).Offset(1, 0).Select
                ActiveCell.FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
            Range("G" & Rows.Count).End(xlUp).Select
                ActiveCell.FormulaR1C1 = "=HOUR(RC[8])*60+MINUTE(RC[8])"
                ActiveCell = ActiveCell.Value
                
                    TD = OT - (BT - ST)
                
                Sheets("NOVO").Select
                    ActiveCell.Offset(0, 12).Select
                    ActiveCell = TD
                    ActiveCell.Offset(0, -8).Select
                    ActiveCell = "=HOUR(RC[8])*60+MINUTE(RC[8])"
                                       
                    ActiveCell = ActiveCell.Value
                    ActiveCell.Offset(-1, -4).Select
                    
               ' UBACIVANJE PAUZE
               
                Sheets("KALENDAR MASINA").Select
                    Range("AA1:AP1").Copy
                    Sheets("PLAN").Select
                    
                    Range("A" & Rows.Count).End(xlUp).Offset(1, 0).Select
                        Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
                    :=False, Transpose:=False
                
                    Range("P" & Rows.Count).End(xlUp) = Range("P" & Rows.Count).End(xlUp).Offset(-1, 0).Value
                
                    Range("A" & Rows.Count).End(xlUp).Offset(1, 0) = 0
                                
                    Range("R" & Rows.Count).End(xlUp).Offset(1, 0).Select
                    ActiveCell.FormulaR1C1 = "=R[-1]C+RC[-3]"
            
                    Range("S" & Rows.Count).End(xlUp).Offset(1, 0).Select
                    ActiveCell.FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
                    
                    Call Format_Pauza
                    
                    
            Y = Y + 1
           
            Sheets("NOVO").Select
            ActiveCell.Offset(1, 0).Select
            X = ActiveCell.Row - 1
               
               
    'CASE 6 - Ubaci neradnu smjenu
               
    ElseIf (STWS = "n") And (BTWS = "n") Then
               
                Sheets("KALENDAR MASINA").Select
                    Range("AA2:AP2").Copy
                    Sheets("PLAN").Select
                    
                    Range("A" & Rows.Count).End(xlUp).Offset(1, 0).Select
                        Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
                    :=False, Transpose:=False
                
                    Range("P" & Rows.Count).End(xlUp) = Range("P" & Rows.Count).End(xlUp).Offset(-1, 0).Value
                
                    Range("A" & Rows.Count).End(xlUp).Offset(1, 0) = 0
                                
                    Range("R" & Rows.Count).End(xlUp).Offset(1, 0).Select
                    ActiveCell.FormulaR1C1 = "=R[-1]C+RC[-3]"
            
                    Range("S" & Rows.Count).End(xlUp).Offset(1, 0).Select
                    ActiveCell.FormulaR1C1 = "=TIME(HOUR(RC[-1]),MINUTE(RC[-1]),0)"
                    
                    Call Format_Neradno
                    
                    Sheets("NOVO").Select
                               
    End If
    
        

Loop
    
        
Unload Progress

    Sheets("PLAN").Select
    
    Range("T5").Select
        ActiveCell.FormulaR1C1 = "=RC[-4]-(RC[-2]-RC[-1])"
    Range("Q5").Select
        ActiveCell.FormulaR1C1 = "=R[-1]C[1]"
   
    Range("R5").Select
    Range(Selection, Selection.End(xlDown)).Select
    n = Selection.Count + 4
       
    Range("T5").Select
    Selection.AutoFill Destination:=Range("T5", Cells(n, 20)), Type:=xlFillValues
    Range("Q5").Select
    Selection.AutoFill Destination:=Range("Q5", Cells(n, 17)), Type:=xlFillValues


Application.Calculation = xlAutomatic
    
Else

MsgBox "Neradna smjena, unesite novi datum i vrijeme ili podesite radne smjene!"
    
End If

Sheets("PRINT").Select
    
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

