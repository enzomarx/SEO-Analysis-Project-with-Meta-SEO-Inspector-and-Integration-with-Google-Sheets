document.getElementById('seo-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const url = document.getElementById('url-input').value.trim();
    if (url === '') {
        alert('Por favor, insira uma URL válida.');
        return;
    }
    fetchSEOData(url);
});

async function fetchSEOData(url) {
    try {
        const response = await fetch(`/api/seo?url=${encodeURIComponent(url)}`);
        const data = await response.json();
        displaySEOData(data);
    } catch (error) {
        console.error('Erro ao buscar dados SEO:', error);
    }
}

function displaySEOData(seoData) {
    const seoResults = document.getElementById('seo-results');
    seoResults.innerHTML = `
        <h2>Resultados para ${seoData.url}</h2>
        <p>Title: ${seoData.title}</p>
        <p>Description: ${seoData.description}</p>
        <p>Total de Links: ${seoData.links.total}</p>
        <p>Links Internos: ${seoData.links.internal}</p>
        <p>Links Externos: ${seoData.links.external}</p>
    `;
}
