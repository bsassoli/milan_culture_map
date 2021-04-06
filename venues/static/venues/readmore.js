document.addEventListener('DOMContentLoaded', () => {
    readmore_btn = document.querySelector('.read-more');
    readmore_btn.addEventListener('click', () => {
        if (readmore_btn.dataset.status==="more") {
        full_text = readmore_btn.dataset.description;
        document.querySelector('#description').innerHTML = full_text;
        readmore_btn.innerHTML = "Leggi di meno";
        readmore_btn.dataset.status="less";
        document.querySelector('#description').append(readmore_btn);
        }
        else {
            less = readmore_btn.dataset.less;
            readmore_btn.innerHTML = "Leggi di più";
            document.querySelector('#description').innerHTML = less;
            readmore_btn.dataset.status="more";
            document.querySelector('#description').append(readmore_btn);
            }
    })
})