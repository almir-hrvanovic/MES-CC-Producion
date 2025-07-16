Attribute VB_Name = "Status_nova_masina"
Sub PROMJENA()
Attribute PROMJENA.VB_ProcData.VB_Invoke_Func = " \n14"


Application.ScreenUpdating = False

    Dim KPL As String
    Dim POZ As String
    Dim NAZIV As String
    Dim MASINA As String
    
    
           
    Col = ActiveCell.Column
   
    If Col = 3 Then

        MASINA = InputBox("Unesi ŠIFRU mašine!")
        KPL = ActiveCell.Value
        POZ = ActiveCell.Offset(0, 2).Value
        NAZIV = ActiveCell.Offset(0, 3).Value
        Item = Right(ActiveCell.Offset(0, 18), 6)
        
        ActiveCell.Interior.Color = rgbBlue
     
   
        Sheets("PROMJENA").Select
   
        Range("A" & Rows.Count).End(xlUp).Offset(1, 0) = KPL & "-" & POZ
        Range("B" & Rows.Count).End(xlUp).Offset(1, 0) = NAZIV
        Range("B" & Rows.Count).End(xlUp).Offset(0, 1) = Item
        Range("B" & Rows.Count).End(xlUp).Offset(0, 2) = MASINA
        
   
        Else
   
        MsgBox "Odaberi radni nalog SKLOPA!"
   
    End If
   
        Sheets("PRINT").Select
   
End Sub
