Attribute VB_Name = "Status_zavsren_sklop"
Sub KPL_Zavrsen()
Attribute KPL_Zavrsen.VB_ProcData.VB_Invoke_Func = " \n14"


Application.ScreenUpdating = False

    Dim KPL As String
    Dim POZ As String
    Dim NAZIV As String

    Col = ActiveCell.Column
   
    If Col = 3 Then
   
        KPL = ActiveCell.Value
        POZ = ActiveCell.Offset(0, 2).Value
        NAZIV = ActiveCell.Offset(0, 3).Value
   
        ActiveCell.Interior.Color = rgbOrange
   
        Sheets("PROMJENA").Select
   
        Range("A" & Rows.Count).End(xlUp).Offset(1, 0) = KPL & "-" & POZ
        Range("B" & Rows.Count).End(xlUp).Offset(1, 0) = NAZIV
   
        Range("A" & Rows.Count).End(xlUp).Interior.Color = rgbOrange
        Range("B" & Rows.Count).End(xlUp).Interior.Color = rgbOrange
   
    Else
    
        MsgBox "Odaberi radni nalog SKLOPA!"
    
    End If
  
        Sheets("PRINT").Select
   
End Sub
