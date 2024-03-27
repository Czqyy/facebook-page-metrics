document.addEventListener('DOMContentLoaded', () => {    
    const spinner = document.getElementById('spinner');
    const generate_btn = document.getElementById('generate_btn');
    const download_btn = document.getElementById('download_btn');
    const status = document.getElementById('status_message');

    document.getElementById('generate').addEventListener('submit', (event) => {
        event.preventDefault();

        let error = document.getElementById('error_message');
        if (error) {
            error.remove()
        }

        status.innerHTML = 'Generating excel...';

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = () => {
            console.log(xhttp.readyState);
            if (xhttp.readyState == 4) {
                console.log("DONE");
                status.innerHTML = '';
                spinner.style.display = 'none';
                download_btn.disabled = false;

                if (xhttp.status == 200) {
                    alert('Excel generated.');
                } else {
                    alert('Something went wrong.');
                }
            }
        };

        spinner.style.display = 'block';
        generate_btn.disabled = true;
        download_btn.disabled = true;

        xhttp.open('GET', `${window.location.href}generate`);
        xhttp.send();
    })

    document.getElementById('download').addEventListener('submit', () => {
        generate_btn.disabled = false;
    })
})