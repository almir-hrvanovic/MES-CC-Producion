Attribute VB_Name = "Azuriraj_crteze"
Sub PDF()

Application.ScreenUpdating = False

Dim Z As Integer
Dim CurrentProgress As Double
Dim ProgressPercentage As Double
Dim BarWidth As Long

Columns("AA:AA").Select
    Selection.EntireColumn.Hidden = False

Z = Application.WorksheetFunction.Count(Range("O5", Range("O5").End(xlDown))) + 4
Range("AA:AA").ClearContents
Columns("U:U").Hyperlinks.Delete

Range("U5").FormulaR1C1 = "=IFERROR(INDEX(NOVO!C[-6],MATCH(PRINT!RC[-16],NOVO!C[-18],0)),"""")"
    Range("U5").AutoFill Destination:=Range("U5", Cells(Z, 21)), Type:=xlFillValues
 
Dim oFSO As Object
Dim oFolder As Object
Dim oFile As Object
Dim i As Integer
 
Set oFSO = CreateObject("Scripting.FileSystemObject")
 
Set oFolder = oFSO.GetFolder("\\192.168.0.5\Priprema\001-PROIZVODNJA\PDF-MASINE\G1000-Mali_Kekeisen")

For Each oFile In oFolder.Files
 
    Cells(i + 1, 27) = oFile.Name
    
    ActiveSheet.Hyperlinks.Add Anchor:=Cells(i + 1, 27), Address:= _
        "\\192.168.0.5\Priprema\001-PROIZVODNJA\PDF-MASINE\G1000-Mali_Kekeisen\" & Cells(i + 1, 27) _
        , TextToDisplay:=Left(oFile.Name, 6)
    Cells(i + 1, 27).Select
    'Selection.Hyperlinks(1).Address = "PDF-MASINE\G1000-Mali_Kekeisen\153757.pdf"
        
    i = i + 1
  
Next oFile

Call InitProgressBar



    Dim Foundcell As Range
    
    For j = 5 To Z

    CurrentProgress = j / Z
    BarWidth = Progress.Border.Width * CurrentProgress
    ProgressPercentage = Round(CurrentProgress * 100, 0)
        
    Progress.Bar.Width = BarWidth
    Progress.Text.Caption = ProgressPercentage & "%"
    DoEvents
    
        Item = Cells(j, 21).Value
     
        If Application.WorksheetFunction.IsNumber(Item) Then
     
            Set Foundcell = Range("AA:AA").Find(What:=Item)
     
                If Foundcell Is Nothing Then
                
                Else
                        
                Range("AA:AA").Find(What:=Item).Copy
                Cells(j, 21).PasteSpecial xlPasteAll
                
                       
                End If
        
        End If

    Next j
  
Unload Progress

Columns("AA:AA").Select
    Selection.EntireColumn.Hidden = True
  
End Sub

Sub InitProgressBar()

With Progress
    .Bar.Width = 0
    .Text.Caption = "0% Završeno!"
    .Show vbModeless
End With

End Sub
