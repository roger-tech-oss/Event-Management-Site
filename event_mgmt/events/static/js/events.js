function selectEvent(eventId) {
    // For now, just mock data:
    document.getElementById('event-detail').innerHTML = `
        <h4>Event #${eventId}</h4>
        <p>More details will appear here...</p>
    `;

    document.getElementById('suggestions').innerHTML = `
        <p>Suggestion 1 for event ${eventId}</p>
        <p>Suggestion 2 for event ${eventId}</p>
    `;
}
