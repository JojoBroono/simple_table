<template>
  <div class="container" id="app">
    <form @submit.prevent="onClick" class="form">
      <p v-if="this.form_errors.length">
        <b>Please correct the following error(s):</b>
        <ul>
          <li v-for="error in this.form_errors" :key="error">{{ error }}</li>
        </ul>
      </p>
      <label for="order_by">Сортировать по</label>
      <select class="select" name="" id="order_by" v-model="order_by">
        <option value="name">Название</option>
        <option value="amount">Количество</option>
        <option value="distance">Расстояние</option>
        <option value="">None</option>
      </select>
      <label for="filter_by">Фильтровать по</label>
      <select class="select" name="" id="filter_by" v-model="filter_by">
        <option value="dt">Дата</option>
        <option value="name">Название</option>
        <option value="amount">Количество</option>
        <option value="distance">Расстояние</option>
        <option value="">None</option>
      </select>
      <label for="filter_condition">Условие</label>
      <select class="select" name="" id="filter_condition" v-model="filter_condition">
        <option value="equal">Равно</option>
        <option value="greater">Больше</option>
        <option value="less">Меньше</option>
        <option value="contains">Содержит</option>
        <option value="">None</option>
      </select>
      <label for="filter_value">Значение</label>
      <input class="input" type="text" v-model="filter_value" id="filter_value">
      <button type="submit">get</button>
    </form>
    
    <div v-if="this.items.length">
      <table class="table">
        <tr>
          <th>Дата</th>
          <th>Название</th>
          <th>Количество</th>
          <th>Расстояние</th>
        </tr>
        <tr v-for="item in this.paginated_items" :key="item">
          <td> {{item.dt}} </td>
          <td> {{item.name}} </td>
          <td> {{item.amount}} </td>
          <td> {{item.distance}} </td>
        </tr>
      </table>
    </div>
    <div v-if="!this.items.length">
      Ничего не нашлось
    </div>


    <p>Страница {{Number(this.page_number) + 1}} из {{Math.ceil(this.items.length / Number(this.elements_on_page))}}</p>
    <p>Перейти на страницу <input type="text" v-model="page_to_go"><button @click="goToPage">Go</button></p>
    
  </div>
  
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
      items: [],
      paginated_items: [],
      order_by: '',
      filter_by: '',
      filter_condition: '',
      filter_value: '',
      form_errors: [],
      page_number: 0,
      elements_on_page: 4,
      page_to_go: 0
    }
  },
  async mounted() {
    await fetch('http://localhost:8000/api/')
        .then(response => response.json())
        .then(json => {
          this.items = json
        });
    const start = this.page_number * this.elements_on_page;
    const end = start + this.elements_on_page;
    this.paginated_items = this.items.slice(start, end);
  },
  components: {
    
  },
  methods: {
    async onClick() {
      this.checkForm()
      if (this.form_errors.length) {
        return
      }
      let api_url = 'http://localhost:8000/api/?'
      if (this.order_by) {
        api_url = api_url + 'order_by=' + this.order_by
      }
      if (this.filter_by && this.filter_condition && this.filter_value) {
        api_url = api_url + '&filter_by=' + this.filter_by + '&condition=' + this.filter_condition + '&val=' + this.filter_value
      }
      await fetch(api_url)
        .then(response => response.json())
        .then(json => {
          this.items = json
        });
      this.page_number = 0;
      this.updatePage();
      
    },
    checkForm() {
      this.form_errors = []

      if (
        (this.filter_by || this.filter_condition || this.filter_value) 
          && !(this.filter_by && this.filter_condition && this.filter_value)
      ) {
        this.form_errors.push('Для фильтрации необходимо заполнить все 3 поля')
      } 
      let DateRegexp = /^(19|20)?[0-9]{2}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$/;
      if (this.filter_by === 'dt' && this.filter_value && !this.filter_value.match(DateRegexp)) {
        this.form_errors.push('Неверный формат даты')
      }
      let IntegerRegexp = /^\d+$/;
      if ((this.filter_by === 'amount' || this.filter_by === 'distance') && this.filter_value && !this.filter_value.match(IntegerRegexp)) {
        this.form_errors.push('Количество и расстояние должны быть положительным целым числом')
      }

    },
    goToPage() {
      this.page_number = Number(this.page_to_go) - 1;
      this.updatePage()
    },
    updatePage() {
      const start = this.page_number * this.elements_on_page;
      const end = start + this.elements_on_page;
      this.paginated_items = this.items.slice(start, end);
    }
  }
}


</script>

<style>

.container {
  margin: 0 auto;
  padding: 80px 0;
  width: 1170px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.table {
	width: 100%;
	margin-bottom: 20px;
	border: 1px solid #dddddd;
	border-collapse: collapse; 

}

.table th {
	font-weight: bold;
	padding: 5px;
	background: #efefef;
	border: 1px solid #dddddd;
}

.table td {
	border: 1px solid #dddddd;
	padding: 5px;
}

.form {
  display: flex;
  flex-direction: column;
  width: 300px;
  margin-bottom: 50px;
}
.select, .input {
  margin-bottom: 10px;
}
</style>
