/**
 * Main JavaScript for Exa GitHub Search
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Form validation enhancements
    const searchForm = document.querySelector('.search-form');

    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            const queryInput = document.getElementById('query');

            if (!queryInput.value.trim()) {
                event.preventDefault();
                showValidationError(queryInput, 'Please enter a search query');
            }
        });

        // Show loading state when form is submitted
        searchForm.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');

            if (submitButton && !submitButton.disabled) {
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Searching...';
                submitButton.disabled = true;
            }
        });
    }

    // Conditional form field toggling based on search type
    const typeSelect = document.getElementById('type');

    if (typeSelect) {
        typeSelect.addEventListener('change', function() {
            toggleFieldsBasedOnSearchType(this.value);
        });

        // Initialize on page load
        toggleFieldsBasedOnSearchType(typeSelect.value);
    }

    // Date field formatting and validation
    const dateFields = document.querySelectorAll('input[name="created"], input[name="pushed"]');

    dateFields.forEach(field => {
        field.addEventListener('blur', function() {
            validateDateFormat(this);
        });
    });

    // Range input validation
    validateRangeInputs('min_stars', 'max_stars');
    validateRangeInputs('min_forks', 'max_forks');
});

/**
 * Show validation error for an input field
 */
function showValidationError(inputElement, message) {
    // Remove any existing error message
    const existingFeedback = inputElement.nextElementSibling;
    if (existingFeedback && existingFeedback.classList.contains('invalid-feedback')) {
        existingFeedback.remove();
    }

    // Add the error class to the input
    inputElement.classList.add('is-invalid');

    // Create and append the error message
    const feedback = document.createElement('div');
    feedback.className = 'invalid-feedback';
    feedback.textContent = message;
    inputElement.parentNode.appendChild(feedback);

    // Focus the input
    inputElement.focus();
}

/**
 * Clear validation error for an input field
 */
function clearValidationError(inputElement) {
    inputElement.classList.remove('is-invalid');

    const existingFeedback = inputElement.nextElementSibling;
    if (existingFeedback && existingFeedback.classList.contains('invalid-feedback')) {
        existingFeedback.remove();
    }
}

/**
 * Toggle form fields based on search type
 */
function toggleFieldsBasedOnSearchType(searchType) {
    const statsSection = document.getElementById('headingStats');
    const statsCollapse = document.getElementById('collapseStats');

    if (!statsSection) return;

    if (searchType === 'repositories') {
        statsSection.style.display = 'block';
    } else {
        statsSection.style.display = 'none';
        if (statsCollapse && statsCollapse.classList.contains('show')) {
            statsCollapse.classList.remove('show');
        }
    }
}

/**
 * Validate date format for GitHub search syntax
 */
function validateDateFormat(inputElement) {
    const value = inputElement.value.trim();

    if (!value) return;

    // GitHub date format patterns (>YYYY-MM-DD, <YYYY-MM-DD, YYYY-MM-DD..YYYY-MM-DD)
    const dateRegex = /^(>|<)?(\d{4}-\d{2}-\d{2})(?:\.\.(\d{4}-\d{2}-\d{2}))?$/;

    if (!dateRegex.test(value)) {
        showValidationError(inputElement, 'Invalid date format. Use >YYYY-MM-DD, <YYYY-MM-DD, or YYYY-MM-DD..YYYY-MM-DD');
    } else {
        clearValidationError(inputElement);
    }
}

/**
 * Validate that min value is less than max value for range inputs
 */
function validateRangeInputs(minFieldId, maxFieldId) {
    const minField = document.getElementById(minFieldId);
    const maxField = document.getElementById(maxFieldId);

    if (!minField || !maxField) return;

    function validateRange() {
        const minValue = parseInt(minField.value) || 0;
        const maxValue = parseInt(maxField.value) || 0;

        if (maxValue > 0 && minValue > maxValue) {
            showValidationError(maxField, 'Maximum value must be greater than minimum value');
            return false;
        } else {
            clearValidationError(maxField);
            return true;
        }
    }

    minField.addEventListener('input', validateRange);
    maxField.addEventListener('input', validateRange);
}

/**
 * Add syntax highlighting to code snippets
 */
function highlightCode() {
    const codeBlocks = document.querySelectorAll('pre code');

    if (window.hljs && codeBlocks.length > 0) {
        codeBlocks.forEach(block => {
            hljs.highlightElement(block);
        });
    }
}