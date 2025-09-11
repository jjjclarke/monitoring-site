document.getElementById('submit-date').addEventListener('click', function() {
    const selectedDate = document.getElementById('date-selector').value;
    if (selectedDate) {
        fetch('/timelapse_route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ date: selectedDate })
        })
        .then(response => response.json())
        .then(data => {
            if (data.video_url) {
                const videoContainer = document.getElementById('video-container');
                videoContainer.innerHTML = ''; // Clear any existing content
                const video = document.createElement('video');
                video.src = data.video_url;
                video.controls = true;
                videoContainer.appendChild(video);
            } else {
                throw new Error(data.error);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert(error.message);
        });
    } else {
        alert('Please select a date.');
    }
});