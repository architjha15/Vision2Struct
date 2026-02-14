document.getElementById('startBtn').addEventListener('click', async function(e) {
    const keyword = document.getElementById('keyword').value;
    const limit = document.getElementById('limit').value;
    
    if (!keyword || !limit) return alert("Please fill all fields!");

    // Show Progress Bar
    const container = document.getElementById('progress-container');
    const bar = document.getElementById('progress-bar');
    const status = document.getElementById('status');
    container.style.display = 'block';

    // 1. Tell the backend to start scraping
    try {
        const response = await fetch('http://localhost:5000/scrape', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keyword, limit })
        });

        // 2. Listen for Progress Updates via SSE (Server-Sent Events)
        const eventSource = new EventSource('http://localhost:5000/progress');

        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            const percent = data.percentage;
            
            bar.style.width = percent + "%";
            status.innerText = `Processing: ${percent}% (${data.message})`;

            if (percent >= 100) {
                eventSource.close();
                status.innerText = "Done! Refreshing...";
                // Small delay so user sees 100% before refresh
                setTimeout(() => {
                    location.reload(); 
                }, 2000);
            }
        };

        eventSource.onerror = function() {
            eventSource.close();
        };

    } catch (error) {
        status.innerText = "Connection failed!";
    }
});