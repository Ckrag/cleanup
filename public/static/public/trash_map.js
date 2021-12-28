function drawPathedNodes(pathed) {
    for (const [route_id, nodes] of pathed.entries()) {
        let path = []
        nodes.forEach((node, i) => {
            path.push([node.lat, node.lng])
            if (path.length === 2) {
                const pl = L.polygon(path).addTo(trashMap)
                pl.bindPopup(node.route_title);
                path = path.slice(1,2)
            }
        })
    }
}

function getPathedNodes(nodes) {
    let paths = new Map();
    nodes.forEach(node => {
        if (!paths.has(node.route_id)) {
            paths.set(node.route_id, []);
        }
        paths.get(node.route_id).push(node);
    })
    return paths;
}

function getRelevantNodes(csrf, lat, lng, latDelta, lngDelta) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/nodes/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader("X-CSRFToken", csrf)
    xhr.onload = function (e) {
        if (xhr.readyState === xhr.DONE) {
            if (xhr.status === 200) {
                let data = JSON.parse(xhr.response)['nodes']
                let pathed = getPathedNodes(data)
                drawPathedNodes(pathed)
            } else {
                alert("Unable to get nodes")
                console.error(xhr.statusText);
            }
        }
    };
    xhr.send(JSON.stringify({
        "lat": lat,
        "lng": lng,
        "lat_delta": latDelta,
        "lng_delta": lngDelta
    }));
}