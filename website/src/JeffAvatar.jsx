// Ejemplo de cómo usar el componente JeffAvatar en tu aplicación React

import React, { useRef } from 'react';
import JeffAvatar from './JeffAvatar';

function App() {
  const avatarRef = useRef();

  const handleMakeTalk = () => {
    // Hacer que hable por 3 segundos
    avatarRef.current?.speak(3000);
  };

  const handleSayHello = () => {
    // Hacer que hable según el texto
    avatarRef.current?.speakText("Hello! I'm Jeff from AWS! Welcome to the cloud!");
  };

  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      gap: '20px',
      padding: '40px'
    }}>
      <h1>Jeff Barr AI Avatar</h1>
      
      {/* Avatar con tamaño personalizado */}
      <JeffAvatar 
        ref={avatarRef}
        size={250} 
        onSpeak={() => console.log('Jeff is speaking!')}
      />
      
      {/* Botones de control */}
      <div style={{ display: 'flex', gap: '10px' }}>
        <button onClick={handleMakeTalk}>
          Make Jeff Talk
        </button>
        <button onClick={handleSayHello}>
          Say Hello
        </button>
      </div>
    </div>
  );
}

export default App;

// ============================================
// OPCIÓN 2: Uso simple sin ref
// ============================================

function SimpleExample() {
  return (
    <div>
      <h2>Simple Jeff Avatar</h2>
      {/* Solo mostrar el avatar sin controles */}
      <JeffAvatar size={200} />
    </div>
  );
}

// ============================================
// OPCIÓN 3: Integrar en tu página existente
// ============================================

function YourExistingPage() {
  return (
    <div className="your-page">
      <header>
        <h1>Your Website</h1>
        {/* Avatar en el header */}
        <JeffAvatar size={150} />
      </header>
      
      <main>
        {/* Tu contenido existente */}
      </main>
      
      <footer>
        {/* Avatar en el footer */}
        <JeffAvatar size={100} />
      </footer>
    </div>
  );
}

