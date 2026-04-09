<template>
  <div class="questions-container">
    <h2>问题设置</h2>
    
    <!-- 添加问题表单 -->
    <div class="form-container">
      <h3>添加新问题</h3>
      <form @submit.prevent="addQuestion">
        <div class="form-group">
          <label for="station_id">所属站点</label>
          <select id="station_id" v-model="newQuestion.station_id" required>
            <option value="">选择站点</option>
            <option v-for="station in stations" :key="station.id" :value="station.id">
              {{ station.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="question">问题</label>
          <textarea id="question" v-model="newQuestion.question" required></textarea>
        </div>
        <div class="form-group">
          <label for="option_a">选项A</label>
          <input type="text" id="option_a" v-model="newQuestion.option_a" required>
        </div>
        <div class="form-group">
          <label for="option_b">选项B</label>
          <input type="text" id="option_b" v-model="newQuestion.option_b" required>
        </div>
        <div class="form-group">
          <label for="option_c">选项C</label>
          <input type="text" id="option_c" v-model="newQuestion.option_c" required>
        </div>
        <div class="form-group">
          <label for="option_d">选项D</label>
          <input type="text" id="option_d" v-model="newQuestion.option_d" required>
        </div>
        <div class="form-group">
          <label for="correct_answer">正确答案</label>
          <select id="correct_answer" v-model="newQuestion.correct_answer" required>
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
            <option value="D">D</option>
          </select>
        </div>
        <div class="form-group">
          <label for="score">分值</label>
          <input type="number" id="score" v-model="newQuestion.score" required>
        </div>
        <button type="submit" class="btn btn-primary">添加问题</button>
      </form>
    </div>
    
    <!-- 问题列表 -->
    <div class="list-container">
      <h3>问题列表</h3>
      <table class="questions-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>所属站点</th>
            <th>问题</th>
            <th>正确答案</th>
            <th>分值</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="question in questions" :key="question.id">
            <td>{{ question.id }}</td>
            <td>{{ getStationName(question.station_id) }}</td>
            <td>{{ question.question }}</td>
            <td>{{ question.correct_answer }}</td>
            <td>{{ question.score }}</td>
            <td>
              <button @click="editQuestion(question)" class="btn btn-edit">编辑</button>
              <button @click="deleteQuestion(question.id)" class="btn btn-delete">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 编辑问题对话框 -->
    <div v-if="editingQuestion" class="modal">
      <div class="modal-content">
        <h3>编辑问题</h3>
        <form @submit.prevent="updateQuestion">
          <div class="form-group">
            <label for="edit-station_id">所属站点</label>
            <select id="edit-station_id" v-model="editingQuestion.station_id" required>
              <option value="">选择站点</option>
              <option v-for="station in stations" :key="station.id" :value="station.id">
                {{ station.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="edit-question">问题</label>
            <textarea id="edit-question" v-model="editingQuestion.question" required></textarea>
          </div>
          <div class="form-group">
            <label for="edit-option_a">选项A</label>
            <input type="text" id="edit-option_a" v-model="editingQuestion.option_a" required>
          </div>
          <div class="form-group">
            <label for="edit-option_b">选项B</label>
            <input type="text" id="edit-option_b" v-model="editingQuestion.option_b" required>
          </div>
          <div class="form-group">
            <label for="edit-option_c">选项C</label>
            <input type="text" id="edit-option_c" v-model="editingQuestion.option_c" required>
          </div>
          <div class="form-group">
            <label for="edit-option_d">选项D</label>
            <input type="text" id="edit-option_d" v-model="editingQuestion.option_d" required>
          </div>
          <div class="form-group">
            <label for="edit-correct_answer">正确答案</label>
            <select id="edit-correct_answer" v-model="editingQuestion.correct_answer" required>
              <option value="A">A</option>
              <option value="B">B</option>
              <option value="C">C</option>
              <option value="D">D</option>
            </select>
          </div>
          <div class="form-group">
            <label for="edit-score">分值</label>
            <input type="number" id="edit-score" v-model="editingQuestion.score" required>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">保存</button>
            <button type="button" @click="editingQuestion = null" class="btn btn-cancel">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Questions',
  data() {
    return {
      questions: [],
      stations: [],
      newQuestion: {
        station_id: '',
        question: '',
        option_a: '',
        option_b: '',
        option_c: '',
        option_d: '',
        correct_answer: 'A',
        score: 10
      },
      editingQuestion: null
    }
  },
  mounted() {
    this.fetchStations()
    this.fetchQuestions()
  },
  methods: {
    async fetchStations() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/admin/stations', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!response.ok) throw new Error('获取站点失败')
        this.stations = await response.json()
      } catch (error) {
        console.error('获取站点失败:', error)
        alert('获取站点失败')
      }
    },
    async fetchQuestions() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/admin/questions', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!response.ok) throw new Error('获取问题失败')
        this.questions = await response.json()
      } catch (error) {
        console.error('获取问题失败:', error)
        alert('获取问题失败')
      }
    },
    getStationName(stationId) {
      const station = this.stations.find(s => s.id === stationId)
      return station ? station.name : '未知站点'
    },
    async addQuestion() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/admin/questions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.newQuestion)
        })
        if (!response.ok) throw new Error('添加问题失败')
        const newQuestion = await response.json()
        this.questions.push(newQuestion)
        this.newQuestion = {
          station_id: '',
          question: '',
          option_a: '',
          option_b: '',
          option_c: '',
          option_d: '',
          correct_answer: 'A',
          score: 10
        }
        alert('问题添加成功')
      } catch (error) {
        console.error('添加问题失败:', error)
        alert('添加问题失败')
      }
    },
    editQuestion(question) {
      this.editingQuestion = { ...question }
    },
    async updateQuestion() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`http://localhost:8000/admin/questions/${this.editingQuestion.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.editingQuestion)
        })
        if (!response.ok) throw new Error('更新问题失败')
        const updatedQuestion = await response.json()
        const index = this.questions.findIndex(q => q.id === updatedQuestion.id)
        if (index !== -1) {
          this.questions[index] = updatedQuestion
        }
        this.editingQuestion = null
        alert('问题更新成功')
      } catch (error) {
        console.error('更新问题失败:', error)
        alert('更新问题失败')
      }
    },
    async deleteQuestion(questionId) {
      if (!confirm('确定要删除这个问题吗？')) return
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`http://localhost:8000/admin/questions/${questionId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!response.ok) throw new Error('删除问题失败')
        this.questions = this.questions.filter(q => q.id !== questionId)
        alert('问题删除成功')
      } catch (error) {
        console.error('删除问题失败:', error)
        alert('删除问题失败')
      }
    }
  }
}
</script>

<style scoped>
.questions-container {
  max-width: 1000px;
  margin: 0 auto;
}

.form-container {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-group textarea {
  height: 100px;
  resize: vertical;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
}

.btn-edit {
  background-color: #2196F3;
  color: white;
  margin-right: 10px;
}

.btn-edit:hover {
  background-color: #0b7dda;
}

.btn-delete {
  background-color: #f44336;
  color: white;
}

.btn-delete:hover {
  background-color: #da190b;
}

.btn-cancel {
  background-color: #9e9e9e;
  color: white;
  margin-left: 10px;
}

.btn-cancel:hover {
  background-color: #757575;
}

.list-container {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.questions-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.questions-table th,
.questions-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.questions-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.questions-table tr:hover {
  background-color: #f5f5f5;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .questions-table {
    font-size: 14px;
  }
  
  .questions-table th,
  .questions-table td {
    padding: 8px;
  }
  
  .btn {
    padding: 8px 12px;
    font-size: 14px;
  }
}
</style>
