document.addEventListener('DOMContentLoaded', () => {
  const subjectsSection = document.getElementById('subjectsSection');
  const addSubjectBtn = document.getElementById('addSubject');

  addSubjectBtn.addEventListener('click', () => {
    const newEntry = subjectsSection.querySelector('.subject-entry').cloneNode(true);
    newEntry.querySelectorAll('input, select').forEach(el => el.value = '');
    subjectsSection.appendChild(newEntry);
  });

  subjectsSection.addEventListener('click', e => {
    if(e.target.classList.contains('remove-subject')) {
      e.target.closest('.subject-entry').remove();
    }
  });

  const ecaSection = document.getElementById('ecaSection');
  const addEcaBtn = document.getElementById('addECA');

  addEcaBtn.addEventListener('click', () => {
    const newEntry = ecaSection.querySelector('.eca-entry').cloneNode(true);
    newEntry.querySelectorAll('input, select').forEach(el => el.value = '');
    ecaSection.appendChild(newEntry);
  });

  ecaSection.addEventListener('click', e => {
    if(e.target.classList.contains('remove-eca')) {
      e.target.closest('.eca-entry').remove();
    }
  });

  // Submit form
  const form = document.getElementById('calcForm');
  form.addEventListener('submit', async e => {
    e.preventDefault();

    const subjects = Array.from(subjectsSection.querySelectorAll('.subject-entry')).map(entry => ({
      type: entry.querySelector('[name="subject_type"]').value,
      name: entry.querySelector('[name="subject_name"]').value,
      grade: entry.querySelector('[name="subject_grade"]').value
    }));

    const ecas = Array.from(ecaSection.querySelectorAll('.eca-entry')).map(entry => ({
      type: entry.querySelector('[name="eca_type"]').value,
      level: entry.querySelector('[name="eca_level"]').value,
      field: entry.querySelector('[name="eca_field"]').value,
      notes: entry.querySelector('[name="eca_notes"]').value
    }));

    const data = {
      subjects,
      ecas,
      sat: form.sat.value
    };

    // Send data to backend
    try {
      const response = await fetch('/calculate', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(data)
      });

      const result = await response.json();
      document.getElementById('result').innerText = `Total Score: ${result.total_score}\nAI Analysis: ${result.ai_analysis}`;
    } catch (err) {
      document.getElementById('result').innerText = 'Error calculating score. Make sure backend is running.';
    }
  });
});
