VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Sheet9"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Private Sub Worksheet_Change(ByVal Target As Range)

'Update 20140722

Dim WorkRng As Range
Dim Rng As Range
Dim xOffsetColumn As Integer
Set WorkRng = Intersect(Application.ActiveSheet.Range("A:A"), Target)
xOffsetColumn = 4
If Not WorkRng Is Nothing Then
    Application.EnableEvents = False
    For Each Rng In WorkRng
        If Not VBA.IsEmpty(Rng.Value) Then
            Rng.Offset(0, xOffsetColumn).Value = Now
            Rng.Offset(0, xOffsetColumn).NumberFormat = "dd-mm-yyyy, hh:mm:ss"
        Else
            Rng.Offset(0, xOffsetColumn).ClearContents
        End If
    Next
    Application.EnableEvents = True
End If
End Sub
