Sub ChangeTextColor()
    Dim doc As Document
    Dim baudot As String
    Dim i As Integer
    Dim textLength As Integer
    
      baudot = "0000110010110001001100001011110010001010110001111001001000010110000100010011001010111001001000001010001110100100011"
    
 
    Set doc = ActiveDocument
    
    
    If doc.Range.Characters.Count = 0 Then
        MsgBox "No text in docx", vbExclamation
        Exit Sub
    End If
    
   
    textLength = doc.Range.Characters.Count
    
    If Len(baudot) <> textLength Then
        If Len(baudot) < textLength Then
            baudot = baudot & String(textLength - Len(baudot), "0")
        Else
            baudot = Left(baudot, textLength)
        End If
    End If
    
    For i = 1 To Len(baudot)
        If Mid(baudot, i, 1) = "1" Then
            doc.Range.Characters(i).Font.Color = RGB(1, 1, 1) ' Black color
        Else
            doc.Range.Characters(i).Font.Color = RGB(0, 0, 0) ' White color
        End If
    Next i
    
    Set doc = Nothing
End Sub

