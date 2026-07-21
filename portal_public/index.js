// Schema definitions for json files
const schemas = {
  // Common fields for simple files
  default: {
    settings: {
      type: 'object',
      fields: {
        galleryMax: { type: 'number', label: 'Max Gallery Items' },
        projectsMax: { type: 'number', label: 'Max Project Items' },
        resourceMax: { type: 'number', label: 'Max Resource Items' }
      }
    },
    courses: {
      type: 'list',
      titleField: 'title',
      fields: {
        title: { type: 'text', label: 'Course Title', required: true },
        description: { type: 'textarea', label: 'Description' },
        buttons: {
          type: 'nested-list',
          label: 'Action Buttons',
          fields: {
            label: { type: 'text', label: 'Button Label' },
            link: { type: 'text', label: 'Link URL' },
            primary: { type: 'boolean', label: 'Primary (Accent) Style' }
          }
        }
      }
    },
    guidelines: {
      type: 'list',
      titleField: 'name',
      fields: {
        name: { type: 'text', label: 'Guideline Name', required: true },
        link: { type: 'text', label: 'PDF Document Link', required: true }
      }
    },
    gallery: {
      type: 'list',
      titleField: 'label',
      fields: {
        image: { type: 'text', label: 'Image Source Path', required: true },
        alt: { type: 'text', label: 'Alternative Image Text' },
        label: { type: 'text', label: 'Display Label' }
      }
    },
    highlights: {
      type: 'list',
      titleField: 'title',
      fields: {
        title: { type: 'text', label: 'Highlight Title', required: true },
        names: { type: 'string-list', label: 'List Items (One per line)' }
      }
    },
    projects: {
      type: 'list',
      titleField: 'title',
      fields: {
        date: { type: 'text', label: 'Date Label' },
        title: { type: 'text', label: 'Project Title', required: true },
        description: { type: 'textarea', label: 'Project Description', required: true },
        readMoreLink: { type: 'text', label: 'Read More Link' }
      }
    },
    resources: {
      type: 'list',
      titleField: 'title',
      fields: {
        id: { type: 'text', label: 'Resource ID', required: true },
        title: { type: 'text', label: 'Title Name', required: true },
        category: { type: 'text', label: 'Category' },
        subtitle: { type: 'text', label: 'Subtitle Description' },
        description: { type: 'textarea', label: 'Full Description', required: true },
        gradient: { type: 'text', label: 'Gradient CSS' },
        initials: { type: 'text', label: 'Short Initials' },
        overview: { type: 'textarea', label: 'Detailed Overview' },
        specs: {
          type: 'nested-list',
          label: 'Specifications',
          fields: {
            key: { type: 'text', label: 'Specification Name' },
            val: { type: 'text', label: 'Specification Value' }
          }
        },
        applications: { type: 'string-list', label: 'Applications (One per line)' }
      }
    }
  },
  // Specific overrides for index.json
  index: {
    settings: {
      type: 'object',
      fields: {
        announcementMax: { type: 'number', label: 'Max Announcement Items' },
        labsMax: { type: 'number', label: 'Max Lab Items' },
        galleryMax: { type: 'number', label: 'Max Gallery Items' },
        projectsMax: { type: 'number', label: 'Max Project Items' },
        policiesMax: { type: 'number', label: 'Max Policy Items' },
        teamMax: { type: 'number', label: 'Max Team Items' }
      }
    },
    announcements: {
      type: 'list',
      titleField: 'title',
      fields: {
        type: { type: 'select', label: 'Announcement Type', options: ['maintainence', 'maintenance', 'event', 'update', 'deadline', 'general'], required: true },
        isNew: { type: 'boolean', label: 'Mark as New' },
        date: { type: 'date', label: 'Announcement Date', required: true },
        title: { type: 'text', label: 'Title text', required: true },
        description: { type: 'textarea', label: 'Detailed Info', required: true },
        linkText: { type: 'text', label: 'Text for Link Button' },
        link: { type: 'text', label: 'Link URL' }
      }
    },
    labs: {
      type: 'list',
      titleField: 'name',
      fields: {
        num: { type: 'text', label: 'Lab Number (e.g. 01)', required: true },
        name: { type: 'text', label: 'Lab Name', required: true },
        image: { type: 'text', label: 'Image URL' },
        room: { type: 'text', label: 'Room Number', required: true },
        title: { type: 'text', label: 'Lab Header Title' },
        description: { type: 'textarea', label: 'Short description text', required: true },
        link: { type: 'text', label: 'Page Link filename (e.g. dc.html)' }
      }
    },
    gallery: {
      type: 'list',
      titleField: 'label',
      fields: {
        category: { type: 'text', label: 'Category Filter Name' },
        image: { type: 'text', label: 'Source Path', required: true },
        alt: { type: 'text', label: 'Alternate Text' },
        label: { type: 'text', label: 'Label title', required: true },
        description: { type: 'textarea', label: 'Brief description' },
        type: { type: 'select', label: 'Asset Type', options: ['image', 'video'], required: true },
        poster: { type: 'text', label: 'Poster image path for video' }
      }
    },
    projects: {
      type: 'list',
      titleField: 'title',
      fields: {
        date: { type: 'text', label: 'Creation Date' },
        title: { type: 'text', label: 'Project Name', required: true },
        description: { type: 'textarea', label: 'Description details', required: true },
        image: { type: 'text', label: 'Cover Image URL' }
      }
    },
    policies: {
      type: 'list',
      titleField: 'name',
      fields: {
        name: { type: 'text', label: 'Policy Name', required: true },
        tag: { type: 'text', label: 'Display Tag Label' },
        link: { type: 'text', label: 'Document Link Path', required: true }
      }
    },
    faq: {
      type: 'list',
      titleField: 'topic',
      fields: {
        topic: { type: 'text', label: 'FAQ Topic Name', required: true },
        questions: { type: 'string-list', label: 'Questions (One per line)' },
        pdfLink: { type: 'text', label: 'Document Link Path' },
        pdfLabel: { type: 'text', label: 'Display Link Label' }
      }
    },
    team: {
      type: 'list',
      titleField: 'name',
      fields: {
        name: { type: 'text', label: 'Team Member Name', required: true },
        role: { type: 'text', label: 'Member Role Title', required: true },
        bio: { type: 'textarea', label: 'Short biography text' },
        photo: { type: 'text', label: 'Profile Photo Path' }
      }
    },
    facilities: {
      type: 'list',
      titleField: 'title',
      fields: {
        num: { type: 'text', label: 'Display Number' },
        title: { type: 'text', label: 'Facility Title Name', required: true },
        items: {
          type: 'nested-list',
          label: 'Linked Labs',
          fields: {
            label: { type: 'text', label: 'Lab Link Name' },
            href: { type: 'text', label: 'Link URL Path' }
          }
        }
      }
    }
  }
};

// Global state
let currentFilename = '';
let currentData = {};
let activeSection = '';
let currentEditIndex = -1;
let currentSHA = '';

// DOM Elements
const fileSelect = document.getElementById('fileSelect');
const editorContainer = document.getElementById('editorContainer');
const sectionList = document.getElementById('sectionList');
const settingsContainer = document.getElementById('settingsContainer');
const settingsForm = document.getElementById('settingsForm');
const listContainer = document.getElementById('listContainer');
const listTitle = document.getElementById('listTitle');
const listTable = document.getElementById('listTable');
const tableHeaderRow = document.getElementById('tableHeaderRow');
const tableBody = document.getElementById('tableBody');
const addItemBtn = document.getElementById('addItemBtn');
const saveBtn = document.getElementById('saveBtn');
const statusAlert = document.getElementById('statusAlert');
const editModal = document.getElementById('editModal');
const itemForm = document.getElementById('itemForm');
const modalTitle = document.getElementById('modalTitle');
const modalFormFields = document.getElementById('modalFormFields');

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
  fetchFileList();
  setupEventListeners();
});

// Fetch list of editable files from server
function fetchFileList() {
  fetch('/content')
    .then(res => res.json())
    .then(files => {
      files.forEach(file => {
        const option = document.createElement('option');
        option.value = file.name;
        option.textContent = file.name;
        fileSelect.appendChild(option);
      });
    })
    .catch(err => showAlert('error', 'Error fetching file list from server'));
}

// Set up UI event listeners
function setupEventListeners() {
  fileSelect.addEventListener('change', (e) => {
    const filename = e.target.value;
    if (filename) {
      loadFile(filename);
    } else {
      editorContainer.classList.add('hidden');
      saveBtn.classList.add('hidden');
    }
  });

  saveBtn.addEventListener('click', saveCurrentFile);

  addItemBtn.addEventListener('click', () => {
    openItemModal(-1);
  });

  // Modal close handlers
  document.querySelectorAll('.close-modal, .close-modal-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      editModal.classList.add('hidden');
    });
  });

  itemForm.addEventListener('submit', handleFormSubmit);
}

// Show validation or response alert banner
function showAlert(type, message) {
  statusAlert.textContent = message;
  statusAlert.className = `alert alert-${type}`;
  statusAlert.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  setTimeout(() => {
    statusAlert.classList.add('hidden');
  }, 5000);
}

// Date helpers and sorting for announcements
function getTodayISO() {
  const d = new Date();
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function parseNoticeDate(dateStr) {
  if (!dateStr) return 0;
  let time = Date.parse(dateStr);
  if (!isNaN(time)) return time;
  const rangeMatch = String(dateStr).match(/^([A-Za-z]+)\s+\d+[\u2013\-]\d+,\s*(\d{4})$/);
  if (rangeMatch) {
    const firstDayMatch = dateStr.match(/\d+/);
    if (firstDayMatch) {
      time = Date.parse(`${rangeMatch[1]} ${firstDayMatch[0]}, ${rangeMatch[2]}`);
      if (!isNaN(time)) return time;
    }
  }
  return 0;
}

function formatDateToISO(dateStr) {
  if (!dateStr) return getTodayISO();
  if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) return dateStr;
  
  const time = parseNoticeDate(dateStr);
  if (time && !isNaN(time)) {
    const d = new Date(time);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
  return getTodayISO();
}

function formatDateToDisplay(dateStr) {
  if (!dateStr) return '';
  if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) {
    const [y, m, d] = dateStr.split('-').map(Number);
    const dateObj = new Date(y, m - 1, d);
    return dateObj.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
  }
  return dateStr;
}

function sortAnnouncements() {
  if (currentData && currentData.announcements && Array.isArray(currentData.announcements)) {
    currentData.announcements.sort((a, b) => parseNoticeDate(b.date) - parseNoticeDate(a.date));
  }
}

// Load JSON data file
function loadFile(filename) {
  fetch(`/content/${filename}`)
    .then(res => {
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      currentSHA = res.headers.get('X-Content-SHA') || res.headers.get('ETag') || '';
      if (currentSHA) {
        currentSHA = currentSHA.replace(/['"]/g, '');
      }
      return res.json();
    })
    .then(data => {
      currentFilename = filename;
      currentData = data;
      sortAnnouncements();
      editorContainer.classList.remove('hidden');
      saveBtn.classList.remove('hidden');
      renderSections();
    })
    .catch(err => showAlert('error', `Error loading file: ${err.message}`));
}

// Render left navigation sidebar sections
function renderSections() {
  sectionList.innerHTML = '';
  const sections = Object.keys(currentData);
  
  sections.forEach((section, index) => {
    // Skip credits as it is not editable
    if (section === 'credits') return;

    const li = document.createElement('li');
    li.textContent = section.charAt(0).toUpperCase() + section.slice(1);
    li.dataset.section = section;
    if (index === 0 || (index === 1 && sections[0] === 'credits')) {
      li.classList.add('active');
      activeSection = section;
    }
    li.addEventListener('click', (e) => {
      document.querySelectorAll('#sectionList li').forEach(item => item.classList.remove('active'));
      li.classList.add('active');
      activeSection = section;
      showSection(section);
    });
    sectionList.appendChild(li);
  });

  if (activeSection) {
    showSection(activeSection);
  }
}

// Switch active panel viewport
function showSection(section) {
  const schema = getSchemaFor(section);
  
  if (schema && schema.type === 'object') {
    listContainer.classList.add('hidden');
    settingsContainer.classList.remove('hidden');
    renderSettingsForm(section, schema);
  } else {
    settingsContainer.classList.add('hidden');
    listContainer.classList.remove('hidden');
    renderListTable(section, schema);
  }
}

// Resolve matching schema or build dynamic fallback
function getSchemaFor(section) {
  const fileKey = currentFilename.replace('.json', '');
  if (schemas[fileKey] && schemas[fileKey][section]) {
    return schemas[fileKey][section];
  }
  if (schemas.default[section]) {
    return schemas.default[section];
  }
  
  // Dynamic fallback schema parser
  const sample = currentData[section];
  if (typeof sample === 'object' && !Array.isArray(sample) && sample !== null) {
    const fields = {};
    Object.keys(sample).forEach(key => {
      fields[key] = { type: typeof sample[key] === 'number' ? 'number' : 'text', label: key };
    });
    return { type: 'object', fields };
  } else if (Array.isArray(sample)) {
    const fields = {};
    if (sample.length > 0 && typeof sample[0] === 'object') {
      Object.keys(sample[0]).forEach(key => {
        if (Array.isArray(sample[0][key])) {
          if (typeof sample[0][key][0] === 'object') {
            fields[key] = { type: 'nested-list', label: key, fields: { label: { type: 'text' }, link: { type: 'text' } } };
          } else {
            fields[key] = { type: 'string-list', label: key };
          }
        } else if (typeof sample[0][key] === 'boolean') {
          fields[key] = { type: 'boolean', label: key };
        } else {
          fields[key] = { type: typeof sample[0][key] === 'number' ? 'number' : 'text', label: key };
        }
      });
    }
    return { type: 'list', titleField: Object.keys(fields)[0] || 'title', fields };
  }
  return null;
}

// Render settings form layout
function renderSettingsForm(section, schema) {
  settingsForm.innerHTML = '';
  const obj = currentData[section] || {};

  Object.keys(schema.fields).forEach(key => {
    const fieldSchema = schema.fields[key];
    const label = document.createElement('label');
    label.textContent = fieldSchema.label || key;

    const input = document.createElement('input');
    input.type = fieldSchema.type === 'number' ? 'number' : 'text';
    input.value = obj[key] !== undefined ? obj[key] : '';
    input.dataset.key = key;

    // Track state modifications instantly
    input.addEventListener('input', (e) => {
      const val = e.target.value;
      currentData[section][key] = fieldSchema.type === 'number' ? Number(val) : val;
    });

    settingsForm.appendChild(label);
    settingsForm.appendChild(input);
  });
}

// Render data collection lists inside a grid table
function renderListTable(section, schema) {
  tableHeaderRow.innerHTML = '';
  tableBody.innerHTML = '';

  if (section === 'announcements') {
    sortAnnouncements();
  }

  const list = currentData[section] || [];
  listTitle.textContent = section.charAt(0).toUpperCase() + section.slice(1);

  if (!schema) return;

  // Render headers
  const headerKeys = Object.keys(schema.fields).filter(k => schema.fields[k].type !== 'nested-list');
  headerKeys.forEach(key => {
    const th = document.createElement('th');
    th.textContent = schema.fields[key].label || key;
    tableHeaderRow.appendChild(th);
  });

  const actionsTh = document.createElement('th');
  actionsTh.textContent = 'Actions';
  tableHeaderRow.appendChild(actionsTh);

  // Render list data rows
  list.forEach((item, index) => {
    const tr = document.createElement('tr');

    headerKeys.forEach(key => {
      const td = document.createElement('td');
      const val = item[key];
      if (Array.isArray(val)) {
        td.textContent = `${val.length} items`;
      } else if (typeof val === 'boolean') {
        td.textContent = val ? 'Yes' : 'No';
      } else {
        td.textContent = val !== undefined ? val : '';
      }
      tr.appendChild(td);
    });

    // Action buttons cell
    const actionsTd = document.createElement('td');
    
    const editBtn = document.createElement('button');
    editBtn.textContent = 'Edit';
    editBtn.className = 'btn btn-secondary btn-small';
    editBtn.style.marginRight = '5px';
    editBtn.addEventListener('click', () => openItemModal(index));

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.className = 'btn btn-danger btn-small';
    deleteBtn.addEventListener('click', () => deleteListItem(index));

    actionsTd.appendChild(editBtn);
    actionsTd.appendChild(deleteBtn);
    tr.appendChild(actionsTd);

    tableBody.appendChild(tr);
  });
}

// Open modal popup for item creation or revision
function openItemModal(index) {
  currentEditIndex = index;
  const schema = getSchemaFor(activeSection);
  if (!schema) return;

  modalTitle.textContent = index === -1 ? `Add New ${activeSection.slice(0, -1)}` : `Edit ${activeSection.slice(0, -1)}`;
  modalFormFields.innerHTML = '';

  const item = index === -1 ? {} : (currentData[activeSection][index] || {});

  Object.keys(schema.fields).forEach(key => {
    const field = schema.fields[key];
    const formGroup = document.createElement('div');
    formGroup.className = 'form-group';

    const label = document.createElement('label');
    label.textContent = field.label || key;
    if (field.required) {
      const star = document.createElement('span');
      star.className = 'required-star';
      star.textContent = '*';
      label.appendChild(star);
    }
    formGroup.appendChild(label);

    const val = item[key];

    if (field.type === 'boolean') {
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.checked = !!val;
      checkbox.id = `field_${key}`;
      formGroup.appendChild(checkbox);

    } else if (field.type === 'date') {
      const dateGroup = document.createElement('div');
      dateGroup.className = 'date-input-group';

      const input = document.createElement('input');
      input.type = 'date';
      input.id = `field_${key}`;
      input.value = formatDateToISO(val);
      if (field.required) input.required = true;

      const todayBtn = document.createElement('button');
      todayBtn.type = 'button';
      todayBtn.className = 'btn btn-secondary btn-small btn-today';
      todayBtn.textContent = 'Today';
      todayBtn.title = "Set to today's date";
      todayBtn.addEventListener('click', () => {
        input.value = getTodayISO();
      });

      dateGroup.appendChild(input);
      dateGroup.appendChild(todayBtn);
      formGroup.appendChild(dateGroup);

    } else if (field.type === 'select') {
      const select = document.createElement('select');
      select.id = `field_${key}`;
      if (field.required) select.required = true;
      field.options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt;
        option.textContent = opt;
        if (val === opt) option.selected = true;
        select.appendChild(option);
      });
      formGroup.appendChild(select);

    } else if (field.type === 'textarea') {
      const textarea = document.createElement('textarea');
      textarea.id = `field_${key}`;
      textarea.rows = 4;
      textarea.value = val !== undefined ? val : '';
      if (field.required) textarea.required = true;
      formGroup.appendChild(textarea);

    } else if (field.type === 'string-list') {
      const textarea = document.createElement('textarea');
      textarea.id = `field_${key}`;
      textarea.rows = 4;
      textarea.placeholder = 'Enter each item on a new line';
      textarea.value = Array.isArray(val) ? val.join('\n') : '';
      formGroup.appendChild(textarea);

    } else if (field.type === 'nested-list') {
      const nestedContainer = document.createElement('div');
      nestedContainer.className = 'nested-list-container';
      nestedContainer.id = `field_${key}`;
      
      const subItems = Array.isArray(val) ? val : [];
      
      // Render sub-items list editor UI
      const renderSubRows = () => {
        nestedContainer.innerHTML = '';
        subItems.forEach((subItem, subIndex) => {
          const rowDiv = document.createElement('div');
          rowDiv.className = 'nested-item-row';

          Object.keys(field.fields).forEach(subKey => {
            const subField = field.fields[subKey];
            if (subField.type === 'boolean') {
              const chk = document.createElement('input');
              chk.type = 'checkbox';
              chk.checked = !!subItem[subKey];
              chk.dataset.key = subKey;
              chk.dataset.index = subIndex;
              chk.title = subField.label || subKey;
              chk.addEventListener('change', (e) => {
                subItems[subIndex][subKey] = e.target.checked;
              });
              rowDiv.appendChild(chk);
            } else {
              const inp = document.createElement('input');
              inp.type = 'text';
              inp.placeholder = subField.label || subKey;
              inp.value = subItem[subKey] !== undefined ? subItem[subKey] : '';
              inp.dataset.key = subKey;
              inp.dataset.index = subIndex;
              inp.addEventListener('input', (e) => {
                subItems[subIndex][subKey] = e.target.value;
              });
              rowDiv.appendChild(inp);
            }
          });

          const delSubBtn = document.createElement('button');
          delSubBtn.type = 'button';
          delSubBtn.textContent = 'X';
          delSubBtn.className = 'btn btn-danger btn-small';
          delSubBtn.addEventListener('click', () => {
            subItems.splice(subIndex, 1);
            renderSubRows();
          });
          rowDiv.appendChild(delSubBtn);
          nestedContainer.appendChild(rowDiv);
        });

        const addSubBtn = document.createElement('button');
        addSubBtn.type = 'button';
        addSubBtn.textContent = 'Add Sub-item';
        addSubBtn.className = 'btn btn-secondary btn-small';
        addSubBtn.style.marginTop = '5px';
        addSubBtn.addEventListener('click', () => {
          const newSubItem = {};
          Object.keys(field.fields).forEach(subKey => {
            newSubItem[subKey] = field.fields[subKey].type === 'boolean' ? false : '';
          });
          subItems.push(newSubItem);
          renderSubRows();
        });
        nestedContainer.appendChild(addSubBtn);
      };

      renderSubRows();
      nestedContainer.dataset.val = JSON.stringify(subItems);
      formGroup.appendChild(nestedContainer);

    } else {
      const input = document.createElement('input');
      input.id = `field_${key}`;
      input.type = field.type === 'number' ? 'number' : 'text';
      input.value = val !== undefined ? val : '';
      if (field.required) input.required = true;
      formGroup.appendChild(input);
    }

    modalFormFields.appendChild(formGroup);
  });

  editModal.classList.remove('hidden');
}

// Handle form submission inside editor dialog
function handleFormSubmit(e) {
  e.preventDefault();
  const schema = getSchemaFor(activeSection);
  if (!schema) return;

  const newItem = {};

  for (const key of Object.keys(schema.fields)) {
    const field = schema.fields[key];
    const el = document.getElementById(`field_${key}`);

    if (field.type === 'boolean') {
      newItem[key] = el.checked;
    } else if (field.type === 'date') {
      newItem[key] = formatDateToDisplay(el.value);
    } else if (field.type === 'string-list') {
      newItem[key] = el.value.split('\n').map(line => line.trim()).filter(line => line.length > 0);
    } else if (field.type === 'nested-list') {
      // Collect nested objects through active inputs inside container
      const subItems = [];
      const rows = el.querySelectorAll('.nested-item-row');
      rows.forEach(row => {
        const subObj = {};
        row.querySelectorAll('input').forEach(input => {
          const subKey = input.dataset.key;
          if (input.type === 'checkbox') {
            subObj[subKey] = input.checked;
          } else {
            subObj[subKey] = input.value;
          }
        });
        subItems.push(subObj);
      });
      newItem[key] = subItems;
    } else {
      const val = el.value;
      newItem[key] = field.type === 'number' ? Number(val) : val;
    }
  }

  // Update in-memory copy
  if (currentEditIndex === -1) {
    if (!currentData[activeSection]) {
      currentData[activeSection] = [];
    }
    currentData[activeSection].push(newItem);
  } else {
    currentData[activeSection][currentEditIndex] = newItem;
  }

  if (activeSection === 'announcements') {
    sortAnnouncements();
  }

  editModal.classList.add('hidden');
  renderListTable(activeSection, schema);
}

// Delete item row from local state copy
function deleteListItem(index) {
  if (confirm('Are you sure you want to delete this item?')) {
    currentData[activeSection].splice(index, 1);
    const schema = getSchemaFor(activeSection);
    renderListTable(activeSection, schema);
  }
}

// Commit local state changes to content store
function saveCurrentFile() {
  const headers = {
    'Content-Type': 'application/json'
  };
  if (currentSHA) {
    headers['X-Content-SHA'] = currentSHA;
    headers['If-Match'] = `"${currentSHA}"`;
  }

  fetch(`/content/${currentFilename}`, {
    method: 'PUT',
    headers: headers,
    body: JSON.stringify(currentData)
  })
    .then(res => {
      if (res.status === 409) {
        throw new Error('conflict');
      }
      if (!res.ok) {
        return res.json().then(errData => {
          throw new Error(errData.detail || `HTTP error! status: ${res.status}`);
        });
      }
      return res.json();
    })
    .then(res => {
      if (res.success) {
        currentSHA = res.version || '';
        showAlert('success', 'File saved successfully! Changes are pushed to GitHub.');
      } else {
        showAlert('error', `Error saving: ${res.error || 'Unknown error'}`);
      }
    })
    .catch(err => {
      if (err.message === 'conflict') {
        showAlert('error', 'Conflict detected! This file was modified by someone else since you loaded it. Please reload the page to get the latest updates before saving.');
      } else {
        showAlert('error', `Save request failed: ${err.message}`);
      }
    });
}
