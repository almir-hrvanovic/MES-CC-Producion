Attribute VB_Name = "Status_redoslijed"
Sub REDOSLIJED()

Application.Calculation = xlAutomatic
Application.ScreenUpdating = False

   Dim KPL As String
   Dim POZ As String
   Dim NAZIV As String
   Dim X As Integer
   Dim Y As Integer
   
   
Col = ActiveCell.Column
ActiveCell.Interior.Color = rgbRed
   
If Col = 3 Then
       
       Y = Sheet7.Cells(Rows.Count, 1).End(xlUp).Row + 1
       
       Sheet7.Range("A" & Y) = Y - 1
       'Sheet7.Range("B" & Y) = ActiveCell.Value & "-" & ActiveCell.Offset(0, 2).Value
       Sheet7.Range("B" & Y) = ActiveCell.Value
       Sheet7.Range("C" & Y) = ActiveCell.Offset(0, 3).Value
    For Z = 1 To Y - 1
       Sheet7.Range("D" & Z + 1).FormulaR1C1 = "=COUNTIF(NOVO!C[-3],REDOSLIJED!RC[-2])"

       Sheet7.Range("D" & Z + 1) = Sheet7.Range("D" & Z + 1).Value
    Next Z
   
  ' Prioritet i brisanje nekativnih redova
  
   Sheet7.Select
   
    X = Application.WorksheetFunction.CountIf(Range("D1", Range("D1").End(xlDown)), 0)
        
        If X > 0 Then
    
            Columns("A:D").Select
                Application.CutCopyMode = False
                ActiveWorkbook.Worksheets("REDOSLIJED").Sort.SortFields.Clear
                ActiveWorkbook.Worksheets("REDOSLIJED").Sort.SortFields.Add2 Key:=Range("D:D") _
                , SortOn:=xlSortOnValues, Order:=xlAscending, DataOption:=xlSortNormal
            With ActiveWorkbook.Worksheets("REDOSLIJED").Sort
                .SetRange Range("A:D")
                .Header = xlYes
                .MatchCase = False
                .Orientation = xlTopToBottom
                .SortMethod = xlPinYin
                .Apply
                End With
        
            Range("D2").Select
                
                Do Until ActiveCell.Value = 1
                    ActiveCell.Offset(1, 0).Select
                Loop
                
            X = ActiveCell.Row - 1
            Rows("2:" & X).Delete Shift:=xlUp
    
        End If
    
    Y = Cells(Rows.Count, 1).End(xlUp).Row
    
        For Z = 1 To Y - 1
            Sheet7.Range("A" & Z + 1) = Z
        Next Z
   
   
Else
    
       MsgBox "Odaberi radni nalog SKLOPA!"
       
End If


Application.Calculation = xlManual


Sheet13.Select


End Sub

