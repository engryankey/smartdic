// var word = $("td")

var word = document.querySelectorAll("td")
var field = document.getElementById("dictfield")
var ans = document.getElementById("ja")

for (let index = 0; index < word.length; index++) {
    word[index].addEventListener("click", poppy);
    word[index].addEventListener("click", sub);

}

ans.addEventListener("click", poppy)
ans.addEventListener("click", sub)

function poppy(){
    field.value = this.textContent;
};

function sub(){
    document.getElementById("form").submit();
}



// $('td').click(function() {
//     window.alert("hello");
// })

// window.alert("Welcome");