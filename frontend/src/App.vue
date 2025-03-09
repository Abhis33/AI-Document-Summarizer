<template>
  <div class="app-container">
    <div class="content-wrapper">
      <!-- Header -->
      <header class="app-header">
        <h1 class="app-title">AI Document Summarizer</h1>
        <p class="app-subtitle">Transform your documents into concise, meaningful summaries with the power of AI</p>
      </header>

      <!-- Main Content -->
      <div class="card">
        <div class="space10all">
          <!-- Input Methods Toggle -->
          <div class="input-toggle">
            <button 
              @click="inputMethod = 'text'"
              :class="['toggle-button', inputMethod === 'text' ? 'active' : '']"
            >
              <i class="fas fa-keyboard mr-2"></i>
              Paste Text
            </button>
            <button 
              @click="inputMethod = 'file'"
              :class="['toggle-button', inputMethod === 'file' ? 'active' : '']"
            >
              <i class="fas fa-file-upload mr-2"></i>
              Upload File
            </button>
          </div>

          <!-- Text Input -->
          <div v-if="inputMethod === 'text'" class="p-6">
            <textarea 
              v-model="inputText" 
              placeholder="Paste your document text here..." 
              class="text-input"
            ></textarea>
          </div>

          <!-- File Upload -->
          <div v-else class="p-6">
            <div 
              class="upload-zone"
              :class="{ 'drag-over': isDragging }"
              @click="$refs.fileInput.click()"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleFileDrop($event); isDragging = false"
            >
              <input 
                ref="fileInput"
                type="file" 
                @change="handleFileUpload" 
                class="hidden"
                accept=".txt,.doc,.docx,.pdf"
              >
              <svg class="upload-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p class="text-lg font-medium text-gray-700 mb-2">Drop your file here or click to browse</p>
              <p class="text-sm text-gray-500">Supported formats: TXT, DOC, DOCX, PDF</p>
            </div>
          </div>

          <!-- Options and Submit -->
          <div class="px-6 pb-6 flex items-center gap-4 space10top">
            <select 
              v-model="summaryLength" 
              class="select-input flex-1 p-2 border border-gray-200 rounded-lg"
            >
              <option value="short">Short Summary (25%)</option>
              <option value="medium">Medium Summary (50%)</option>
              <option value="long">Detailed Summary (75%)</option>
            </select>
            <button 
              @click="summarizeText" 
              :disabled="!inputText || isLoading"
              class="btn btn-primary"
            >
              <span v-if="isLoading" class="spinner">⌛</span>
              <span>{{ isLoading ? 'Summarizing...' : 'Summarize' }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Results -->
      <div v-if="summary" class="card results-section p-6">
        <h2 class="summary-title">Summary</h2>
        <div class="summary-content">
          <p class="mb-6">{{ summary }}</p>
          
          <h3 class="text-xl font-bold text-gray-800 mb-4">Key Points</h3>
          <div class="key-points">
            <div 
              v-for="(point, index) in keyPoints" 
              :key="index"
              class="key-point"
            >
              <span class="key-point-bullet">•</span>
              <span>{{ point }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import '@/assets/main.css';

export default {
  data() {
    return {
      inputText: '',
      summaryLength: 'medium',
      summary: '',
      keyPoints: [],
      inputMethod: 'text',
      isLoading: false,
      isDragging: false,
    };
  },
  methods: {
    async summarizeText() {
      if (!this.inputText.trim()) {
        alert('Please enter text to summarize.');
        return;
      }
      
      this.isLoading = true;
      try {
        const response = await axios.post('http://localhost:8000/summarize', {
          text: this.inputText,
          length: this.summaryLength,
        });
        this.summary = response.data.summary;
        this.keyPoints = response.data.key_points;
      } catch (error) {
        console.error('Error summarizing text:', error);
        alert('An error occurred while summarizing the text. Please try again.');
      } finally {
        this.isLoading = false;
      }
    },
    async handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      await this.processFile(file);
    },
    async handleFileDrop(event) {
      const file = event.dataTransfer.files[0];
      if (!file) return;
      await this.processFile(file);
    },
    async processFile(file) {
      const formData = new FormData();
      formData.append('file', file);
      
      this.isLoading = true;
      try {
        const response = await axios.post('http://localhost:8000/upload', formData);
        this.inputText = response.data.text;
        this.inputMethod = 'text'; // Switch to text view after successful upload
      } catch (error) {
        console.error('Error uploading file:', error);
        alert('An error occurred while uploading the file. Please try again.');
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style>
/* Add any custom styles here */
</style>
