function copy() {
    let text = document.getElementById('cpy-input');
    text.select();
    document.execCommand("copy");
    alert('Copied to clipboard');
}

function isValidUrl(string) {
    try {
      new URL(string);
      return true;
    } catch (err) {
      return false;
    }
}

console.log(api);

function shortit(){
    let text = document.getElementById('url-input').value;
    if (isValidUrl(text)){
        fetch(api+'?url='+text)
            .then(response => response.json())
            .then(data => {
                document.getElementById('cpy-input').value = window.location.href+ "o/"+data.id;
                document.getElementById('copy').style.display="flex";
            });

    }
    else {
        alert('no');
    }
}