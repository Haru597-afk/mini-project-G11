# Math Jungle War

เกม Math Jungle War สำหรับเผยแพร่ด้วย GitHub Pages โดยคงเกม HTML/CSS/JavaScript เดิมไว้

## วิธีเผยแพร่บน GitHub Pages

1. สร้าง repository ใหม่บน GitHub เช่น `math-jungle-war`.
2. อัปโหลดไฟล์ทั้งหมดในโฟลเดอร์นี้ไปไว้ที่ **root** ของ repository โดยให้ `index.html` อยู่ระดับบนสุด ไม่ใช่อยู่ในโฟลเดอร์ย่อย.
3. เปิดหน้า repository แล้วไปที่ **Settings → Pages**.
4. ในส่วน **Build and deployment** เลือก **Deploy from a branch**.
5. เลือก branch `main` และ folder `/(root)` แล้วกด **Save**.
6. รอสักครู่ จากนั้นเปิด URL ที่ GitHub Pages แสดงไว้ในหน้า Settings → Pages.

## หมายเหตุ

- GitHub Pages โฮสต์เว็บไซต์แบบ static ได้ จึงใช้ `index.html` โดยตรง ไม่ต้องแปลงเป็น Python.
- คะแนน/Leaderboard ที่เก็บด้วย `localStorage` จะอยู่ในเบราว์เซอร์และอุปกรณ์ของผู้เล่นแต่ละคน ไม่ได้รวมคะแนนจากทุกคนเป็นฐานข้อมูลออนไลน์.
