document.addEventListener('DOMContentLoaded', () => {
  const subjectsSection = document.getElementById('subjectsSection');
  const addSubjectBtn = document.getElementById('addSubject');

  // Add new subject entry
  addSubjectBtn.addEventListener('click', () => {
    const newEntry = subjectsSection.querySelector('.subject-entry').cloneNode(true);
    newEntry.querySelectorAll('input, select').forEach(el => el.value = '');
    subjectsSection.appendChild(newEntry);
  });

  // Remove subject entry
  subjectsSection.addEventListener('click', e => {
    if (e.target.classList.contains('remove-subject')) {
      e.target.closest('.subject-entry').remove();
    }
  });

  const ecaSection = document.getElementById('ecaSection');
  const addEcaBtn = document.getElementById('addECA');

  // Add new ECA entry
  addEcaBtn.addEventListener('click', () => {
    const newEntry = ecaSection.querySelector('.eca-entry').cloneNode(true);
    newEntry.querySelectorAll('input, select').forEach(el => el.value = '');
    ecaSection.appendChild(newEntry);
  });

  // Remove ECA entry
  ecaSection.addEventListener('click', e => {
    if (e.target.classList.contains('remove-eca')) {
      e.target.closest('.eca-entry').remove();
    }
  });

  // Submit form
  const form = document.getElementById('calcForm');
  form.addEventListener('submit', async e => {
    e.preventDefault();

    // Collect O-Level / A-Level subjects
    const subjects = Array.from(subjectsSection.querySelectorAll('.subject-entry')).map(entry => ({
      level: entry.querySelector('[name="subject_level"]').value,
      name: entry.querySelector('[name="subject_name"]').value,
      grade: entry.querySelector('[name="subject_grade"]').value
    }));

    // Collect ECAs
    const ecas = Array.from(ecaSection.querySelectorAll('.eca-entry')).map(entry => ({
      type: entry.querySelector('[name="eca_type"]').value,
      level: entry.querySelector('[name="eca_level"]').value,
      field: entry.querySelector('[name="eca_field"]').value,
      notes: entry.querySelector('[name="eca_notes"]').value
    }));

    // Collect other fields
    const data = {
      program: form.program.value,
      school: form.school.value,
      matric_percentage: form.matric_percentage?.value || 0,
      fsc_percentage: form.fsc_percentage?.value || 0,
      olevel_percentage: form.olevel_percentage?.value || 0,
      alevel_percentage: form.alevel_percentage?.value || 0,
      sat: form.sat.value || 0,
      subjects,
      ecas
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      document.getElementById('result').innerText =
        `Total Score: ${result.total_score}\nAI Analysis: ${result.ai_analysis}`;
    } catch (err) {
      console.error(err);
      document.getElementById('result').innerText =
        'Error calculating score. Make sure backend is running.';
    }
  });
});
