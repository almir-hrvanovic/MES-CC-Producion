Attribute VB_Name = "Dole_gore"
Sub Dole()
Attribute Dole.VB_ProcData.VB_Invoke_Func = " \n14"

Application.ScreenUpdating = False

    Dim i As Integer
    Dim j As Integer
       
    i = Selection.Row
    j = Cells(Rows.Count, 1).End(xlUp).Row

If i >= 2 And i <= j - 1 Then
   
    Range("B" & i, "D" & i).Select
    Selection.Cut
    Range("B" & i + 2, "D" & i + 2).Select
    Selection.Insert Shift:=xlDown
    Range("A" & i + 1, "D" & i + 1).Select
      
Else

    MsgBox "Odaberi podatke od reda 2 do reda " & j - 1
    
End If
    
End Sub
Sub Gore()

Application.ScreenUpdating = False

    Dim i As Integer
    Dim j As Integer
       
    i = Selection.Row
    j = Cells(Rows.Count, 1).End(xlUp).Row

If i >= 3 And i <= j Then
   
    Range("B" & i, "D" & i).Select
    Selection.Cut
    Range("B" & i - 1, "D" & i - 1).Select
    Selection.Insert Shift:=xlDown
    Range("A" & i - 1, "D" & i - 1).Select
      
Else

    MsgBox "Odaberi podatke od reda 3 do reda " & j
    
End If
    
End Sub

Sub Ocisti()

    Range("A2:D2000").ClearContents
   
End Sub


Sub Obrisi_red()

    Application.ScreenUpdating = False

    Dim i As Integer
    Dim j As Integer
       
    i = Selection.Row
    j = Cells(Rows.Count, 1).End(xlUp).Row
  
    Range("B" & i, "D" & i).Select
    Application.CutCopyMode = False
    Selection.Delete Shift:=xlUp
      
    Range("A" & j).Clear
   
End Sub

    

