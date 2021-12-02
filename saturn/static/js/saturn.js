function switchforms(){
    if (document.getElementById("prescriberradio").checked) {
      document.getElementById("prescriberform").style.display = "block";
      document.getElementById("drugform").style.display = "none";
  }
  else if (document.getElementById("drugradio").checked) {
    document.getElementById("prescriberform").style.display = "none";
    document.getElementById("drugform").style.display = "block";
  }
}


// Script to open and close sidebar
function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("myOverlay").style.display = "block";
  }
   
  function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
    document.getElementById("myOverlay").style.display = "none";
  }
  
  // Modal Image Gallery
  function onClick(element) {
    document.getElementById("img01").src = element.src;
    document.getElementById("modal01").style.display = "block";
    var captionText = document.getElementById("caption");
    captionText.innerHTML = element.alt;
  }