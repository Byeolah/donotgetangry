function validate() {
        if($('input[name=pawnnum]:checked').length<=0)
        {
         alert("No radio checked")
            return false
        }
    }