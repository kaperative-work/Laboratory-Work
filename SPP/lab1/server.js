const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

// Автоматическое создание папки для загрузки файлов
const uploadDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

// Настройка хранилища Multer для загружаемых вложений
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
    cb(null, uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({ storage });

// Шаблонизатор и Middleware
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.urlencoded({ extended: true }));
app.use('/uploads', express.static(uploadDir));

// База данных в памяти
let shoppingItems = [
  {
    id: '1',
    title: 'Молоко 2.5% и сыр',
    status: 'pending', // 'pending' или 'bought'
    targetDate: '2026-09-20',
    file: null,
    originalFileName: null
  }
];

// Маршрут: Отображение списка с фильтрацией
app.get('/', (req, res) => {
  const filter = req.query.status || 'all';

  let filteredItems = shoppingItems;
  if (filter === 'pending') {
    filteredItems = shoppingItems.filter(item => item.status === 'pending');
  } else if (filter === 'bought') {
    filteredItems = shoppingItems.filter(item => item.status === 'bought');
  }

  res.render('index', {
    items: filteredItems,
    currentFilter: filter
  });
});

// Маршрут: Добавление позиции через POST-форму
app.post('/add', upload.single('attachment'), (req, res) => {
  const { title, targetDate } = req.body;

  if (title && title.trim() !== '') {
    const newItem = {
      id: Date.now().toString(),
      title: title.trim(),
      status: 'pending',
      targetDate: targetDate || null,
      file: req.file ? `/uploads/${req.file.filename}` : null,
      originalFileName: req.file ? req.file.originalname : null
    };
    shoppingItems.push(newItem);
  }

  res.redirect('/');
});

// Маршрут: Смена статуса (Куплено / Не куплено)
app.post('/toggle-status/:id', (req, res) => {
  const item = shoppingItems.find(i => i.id === req.params.id);
  if (item) {
    item.status = item.status === 'pending' ? 'bought' : 'pending';
  }
  res.redirect(req.get('referer') || '/');
});

// Маршрут: Удаление товара из списка
app.post('/delete/:id', (req, res) => {
  const index = shoppingItems.findIndex(i => i.id === req.params.id);
  if (index !== -1) {
    const item = shoppingItems[index];
    if (item.file) {
      const filePath = path.join(__dirname, item.file);
      if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
      }
    }
    shoppingItems.splice(index, 1);
  }
  res.redirect(req.get('referer') || '/');
});

app.listen(PORT, () => {
  console.log(`Сервер запущен на http://localhost:${PORT}`);
});