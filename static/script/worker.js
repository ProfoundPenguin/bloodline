self.onmessage = function(event) {
    const { theData, searchString, fullData } = event.data;
    const matches = search(theData, searchString, fullData);
    self.postMessage(matches);
};

function search(theData, searchString, fullData, matches = []) {
    if (searchString.length <= 1) {
        return [];
    }

    // Ensure that required properties are present
    if (theData.farsi_name && theData.farsi_name.toLowerCase().includes(searchString.toLowerCase())) {
        matches.push("<li onclick='dramaticZoom(" + theData.id + ")'>" + theData.farsi_name + " (ولد. " + findById(fullData, theData.father).farsi_name + ")" + "</li>");
    } else if (theData.first_name && theData.first_name.toLowerCase().includes(searchString.toLowerCase())) {
        matches.push("<li onclick='dramaticZoom(" + theData.id + ")'>" + theData.farsi_name + " (ولد. " + findById(fullData, theData.father).farsi_name + ")" + "</li>");
    }

    // Recursively search children
    if (theData.children && theData.children.length > 0) {
        for (let i = 0; i < theData.children.length; i++) {
            search(theData.children[i], searchString, fullData, matches);
        }
    }

    return matches;
}

// Dummy findById function for demonstration
function findById(person, targetId) {
    if (person.id === targetId) {
        return person;
    } else if (person.children && person.children.length > 0) {
        for (let i = 0; i < person.children.length; i++) {
            const found = findById(person.children[i], targetId);
            if (found) return found;
        }
    }
    return null;
}
