<template>
  <div class="container mx-auto p-6">
    <h1 class="text-2xl font-bold">AI-Powered Document Summarizer</h1>

    <!-- Text Input -->
    <textarea v-model="inputText" placeholder="Paste text here..." class="w-full p-2 border rounded mt-4"></textarea>

    <!-- File Upload -->
    <input type="file" @change="handleFileUpload" class="mt-4">

    <!-- Summary Length Selection -->
    <select v-model="summaryLength" class="mt-4 p-2 border rounded">
      <option value="short">Short</option>
      <option value="medium">Medium</option>
      <option value="long">Long</option>
    </select>

    <!-- Submit Button -->
    <button @click="summarizeText" class="mt-4 p-2 bg-blue-500 text-white rounded">Summarize</button>

    <!-- Output -->
    <div v-if="summary" class="mt-6 p-4 border rounded">
      <h2 class="text-lg font-bold">Summary</h2>
      <p>{{ summary }}</p>
      <h3 class="text-md font-bold mt-4">Key Points</h3>
      <ul>
        <li v-for="(point, index) in keyPoints" :key="index">- {{ point }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      inputText: '',
      summaryLength: 'medium',
      summary: '',
      keyPoints: [],
    };
  },
  methods: {
    async summarizeText() {
      if (!this.inputText.trim()) {
        alert('Please enter text to summarize.');
        return;
      }
      try {
        const response = await axios.post('http://localhost:8000/summarize', {
          text: this.inputText,
          length: this.summaryLength,
        });
        this.summary = response.data.summary;
        this.keyPoints = response.data.key_points;
      } catch (error) {
        console.error('Error summarizing text:', error);
      }
    },
    async handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      const formData = new FormData();
      formData.append('file', file);
      try {
        const response = await axios.post('http://localhost:8000/upload', formData);
        this.inputText = response.data.text;
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  }
};
</script>

<style>
.container {
  max-width: 600px;
  margin: auto;
}
</style>
