// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    // Select all buttons with the class "content_container"
    let buttons = document.querySelectorAll(".content_container");

    buttons.forEach(button => {
        button.addEventListener("click", function (event) {

            let content = this.parentElement.querySelector(".choice_listing");

            if (content.style.display === "none" || content.style.display === "") {
                content.style.display = "block";
            } else {
                content.style.display = "none";
            }

            event.stopPropagation();
        });
    });

    // Hide any open content dropdown if clicking outside
    document.addEventListener("click", function (event) {

        let allContents = document.querySelectorAll(".choice_listing");
        allContents.forEach(content => {

            if (content.style.display === "block" && !content.contains(event.target)) {
                content.style.display = "none";
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    let return_button = document.querySelector(".return:not([name='return_to_detail'])");
    return_button.addEventListener('click', function(event) {
        window.location.href = "/";;
    })
})


