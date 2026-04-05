// Language redirect CloudFront Function.
// Inspects the Accept-Language header on requests to the root path.
// Redirects to the matching language directory with a 302.
// Values injected by Terraform templatefile():
//   - default_language
//   - supported_languages

const defaultLanguage = '${default_language}';
const supportedLanguages = ${supported_languages};

function handler(event) {
    const request = event.request;
    const uri = request.uri;

    // Append index.html to directory paths.
    if (uri.endsWith('/')) {
        if (uri === '/') {
            // Root path: redirect to language directory.
        } else {
            request.uri = uri + 'index.html';
            return request;
        }
    } else {
        return request;
    }

    const headers = request.headers;
    const acceptLanguage = headers['accept-language']
        ? headers['accept-language'].value
        : '';

    const matched = matchLanguage(acceptLanguage);
    const location = '/' + matched + '/';

    return {
        statusCode: 302,
        statusDescription: 'Found',
        headers: {
            'location': { value: location },
            'cache-control': { value: 'no-store' }
        }
    };
}

// Parses the Accept-Language header and returns the best match.
// The header format is: fr-FR,fr;q=0.9,en;q=0.8,de;q=0.7
// Each entry has an optional quality factor (q).
// Entries without q default to 1.0 (highest priority).
function matchLanguage(header) {
    if (!header) {
        return defaultLanguage;
    }

    const entries = header.split(',');
    const candidates = [];

    for (let i = 0; i < entries.length; i++) {
        const parts = entries[i].trim().split(';');
        const tag = parts[0].trim().toLowerCase();
        let quality = 1.0;

        if (parts.length > 1) {
            const qPart = parts[1].trim();
            if (qPart.indexOf('q=') === 0) {
                quality = parseFloat(qPart.substring(2));
            }
        }

        // Extract the primary language subtag (e.g. fr from fr-FR).
        const primary = tag.split('-')[0];

        candidates.push({ language: primary, quality: quality });
    }

    // Sort by quality descending.
    candidates.sort(function(a, b) {
        return b.quality - a.quality;
    });

    // Return the first supported match.
    for (let j = 0; j < candidates.length; j++) {
        if (supportedLanguages.indexOf(candidates[j].language) !== -1) {
            return candidates[j].language;
        }
    }

    return defaultLanguage;
}
