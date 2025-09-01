import React, { useState } from 'react';
import axios from 'axios';





function App() {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState('');
  const [sections, setSections] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [geminiRaw, setGeminiRaw] = useState(null);
  const [skills, setSkills] = useState([]);
  const [showSkills, setShowSkills] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setSections({});
    setGeminiRaw(null);
    setSkills([]);
    setShowSkills(false);
    setError('');
  };

  const handleJobDescChange = (e) => {
    setJobDesc(e.target.value);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file.');
      return;
    }
    if (!jobDesc.trim()) {
      setError('Please enter a job description.');
      return;
    }
    setLoading(true);
    setError('');
    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_description', jobDesc);
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/upload_resume/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      // Parse Gemini response into sections using regex
      const text = Array.isArray(res.data.questions) ? res.data.questions.join('\n') : (res.data.questions || '').toString();
      const sectionRegex = /\*\*(.+?)\*\*\s*([\s\S]*?)(?=(\*\*|$))/g;
      let match;
      const parsedSections = {};
      while ((match = sectionRegex.exec(text)) !== null) {
        const sectionTitle = match[1].trim();
        // Split questions by lines that start with a number or bullet
        const questions = match[2]
          .split(/\n+/)
          .map(q => q.replace(/^\d+\.|^\*+|^\-+/, '').trim())
          .filter(q => q.length > 0);
        parsedSections[sectionTitle] = questions;
      }
      setSections(parsedSections);
      setGeminiRaw(res.data.gemini_raw || null);
      // Set skills if present in response
      if (Array.isArray(res.data.skills)) {
        setSkills(res.data.skills);
      } else {
        setSkills([]);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed.');
      setGeminiRaw(err.response?.data?.gemini_raw || null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div style={{ maxWidth: 500, margin: '40px auto', padding: 20, border: '1px solid #ccc', borderRadius: 8, position: 'relative', background: '#f8fafc' }}>
        <h2>AI Interview Prep</h2>
        <div style={{ marginBottom: 12 }}>
          <label>Job Description and Custom Instructions:</label>
          <textarea
            value={jobDesc}
            onChange={handleJobDescChange}
            rows={4}
            style={{ width: '100%', marginTop: 4 }}
            placeholder="Paste or type the job description here..."
          />
        </div>
        <input type="file" accept=".pdf,.doc,.docx" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={loading} style={{ marginLeft: 10 }}>
          {loading ? 'Uploading...' : 'Upload Resume'}
        </button>
        {skills.length > 0 && (
          <button
            onClick={() => setShowSkills((prev) => !prev)}
            style={{ marginLeft: 10, padding: '6px 16px', borderRadius: 6, background: '#7c3aed', color: 'white', border: 'none', fontWeight: 600 }}
          >
            {showSkills ? 'Hide Extracted Skills' : 'Show Extracted Skills'}
          </button>
        )}
        {error && <div style={{ color: 'red', marginTop: 10 }}>{error}</div>}
        {geminiRaw && (
          <div style={{ marginTop: 20, background: '#f0f0f0', padding: 10, borderRadius: 6 }}>
            <h4>Raw Gemini API Response:</h4>
            <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all', fontSize: 12 }}>{JSON.stringify(geminiRaw, null, 2)}</pre>
          </div>
        )}
        {/* Skills Sidebar */}
        {skills.length > 0 && showSkills && (
          <div style={{ position: 'absolute', top: 20, right: -320, width: 300, background: '#ede9fe', border: '1px solid #a78bfa', borderRadius: 8, padding: 20, boxShadow: '0 2px 8px #a78bfa55', zIndex: 10 }}>
            <h4 style={{ color: '#7c3aed', marginBottom: 12 }}>Extracted Skills</h4>
            <ul style={{ marginLeft: 18, color: '#444' }}>
              {skills.map((s, i) => <li key={i} style={{ marginBottom: 6 }}>{s}</li>)}
            </ul>
          </div>
        )}
      </div>

      {/* Interview Questions Section - visually distinct and separate */}
      {Object.keys(sections).length > 0 && (
        <div style={{
          maxWidth: 600,
          margin: '32px auto 0 auto',
          padding: 28,
          borderRadius: 16,
          background: 'linear-gradient(135deg, #e0e7ff 0%, #f0abfc 100%)',
          boxShadow: '0 4px 24px #a78bfa33',
          border: '1.5px solid #a78bfa',
        }}>
          <h3 style={{ color: '#6d28d9', fontWeight: 700, fontSize: 24, marginBottom: 18, textAlign: 'center', letterSpacing: 1 }}>Interview Questions</h3>
          {Object.entries(sections).map(([section, qs]) => (
            <div key={section} style={{ marginBottom: 22, padding: 14, background: '#fdf4ff', borderRadius: 8, boxShadow: '0 1px 4px #a78bfa22' }}>
              <h5 style={{ marginBottom: 10, color: '#a21caf', fontWeight: 600, fontSize: 18 }}>{section}</h5>
              <ul style={{ marginLeft: 22, color: '#3b0764', fontSize: 15 }}>
                {qs.map((q, i) => <li key={i} style={{ marginBottom: 7 }}>{q}</li>)}
              </ul>
            </div>
          ))}
        </div>
      )}
    </>
  );
}

export default App;
