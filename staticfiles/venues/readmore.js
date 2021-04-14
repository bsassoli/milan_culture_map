document.addEventListener('DOMContentLoaded', () => {
    readmore_btn = document.querySelectorAll('.read-more');
    readmore_btn.forEach(element =>
    element.addEventListener('click', () => {
        if (element.dataset.status==="more") {
        full_text = element.dataset.description;
        let description = element.parentElement;
        description.innerHTML = full_text;
        console.log(full_text)
        element.innerText = "Leggi di meno";
        element.dataset.status="less";
        description.append(element);
        }
        else {
            let description = element.parentElement;
            less = element.dataset.less;
            element.innerHTML = "Leggi di più";
            description.innerHTML = less;
            element.dataset.status="more";
            description.append(element);
            }
    })
    )
})