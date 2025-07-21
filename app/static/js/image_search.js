

// Map template text to broader SerpAPI search terms
const SerpAPIKeywordMap = {
    'Wake up and smile!': 'morning',
    'Brush your teeth.': 'toothbrush',
    'Get dressed for the day.': 'clothes',
    'Eat a healthy breakfast.': 'breakfast',
    'Go to school and learn.': 'school classroom',
    'Say hello to someone new.': 'greeting',
    'Share your toys.': 'children sharing',
    'Listen to your friends.': 'children talking',
    'Be kind and helpful.': 'helping',
    'Arrive at the clinic.': 'doctor clinic',
    'Wait your turn patiently.': 'waiting room',
    'Talk to the doctor.': 'doctor patient',
    'Get a sticker for being brave!': 'reward sticker',
    'Go to class.': 'school classroom',
    'Listen to the teacher.': 'teacher classroom',
    'Play at recess.': 'children playground',
    'Eat lunch with friends.': 'school lunch',
    'Go home and rest.': 'home',
    'Sometimes I feel happy.': 'happy child',
    'Sometimes I feel sad.': 'sad child',
    "It's okay to talk about feelings.": 'children feelings'
};

// Fetch SerpApi image via Flask backend proxy (avoids CORS issues)
async function fetchSerpApiImage(query) {
    const mapped = SerpAPIKeywordMap[query] || query;
    const url = `/stories/api/serpapi_image?query=${encodeURIComponent(mapped)}`;
    try {
        const response = await fetch(url);
        if (!response.ok) return null;
        const data = await response.json();
        if (data.url) return data.url;
        return null;
    } catch (err) {
        return null;
    }
}
