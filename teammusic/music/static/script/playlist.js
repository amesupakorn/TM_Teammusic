function savePlaylist() {
    // ดึงข้อมูลจากฟิลด์ input
    const name = document.getElementById('playlistName').value;
    const description = document.getElementById('playlistDescription').value;
    const image = document.getElementById('playlistImage').files[0];

    // ตรวจสอบว่าใส่ชื่อ Playlist หรือไม่
    if (!name) {
      alert('Please enter a playlist name');
      return;
    }

    // ส่งข้อมูลไปยัง backend โดยใช้ fetch
    const formData = new FormData();
    formData.append('name', name);
    formData.append('description', description);
    if (image) formData.append('image', image);

    fetch('/teammusic/create_playlist/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': '{{ csrf_token }}' 
      },
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Playlist created successfully!');
      } else {
        alert('Failed to create playlist');
      }
    })
    .catch(error => console.error('Error:', error));
  }

  function previewImage(event) {
    const input = event.target;
    const preview = document.getElementById('imagePreview');
    const uploadIcon = document.getElementById('uploadIcon');

    if (input.files && input.files[0]) {
      const reader = new FileReader();
      
      reader.onload = function(e) {
        preview.src = e.target.result;
        preview.classList.remove('hidden');  // แสดงภาพตัวอย่าง
        uploadIcon.classList.add('hidden');  // ซ่อนไอคอน SVG
      };
      
      reader.readAsDataURL(input.files[0]);
    }
  }