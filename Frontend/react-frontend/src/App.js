import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from  './Component/Dashboard'
import Upload from './Component/Upload'
import Search from './Component/Search'
import Gallery from './Component/Gallery'
import Setting from './Component/Setting'


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="upload" element={<Upload />} />
        <Route path="search" element={<Search />} />
        <Route path="gallery" element={<Gallery />} />
        <Route path="setting" element={<Setting />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App