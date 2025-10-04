import React, { useState } from 'react'

function ChatBot() {
	const [messages, setMessages] = useState([]) // { type: 'user' | 'bot', content: string, sources?: string[] }
	const [input, setInput] = useState('')
	const [loading, setLoading] = useState(false)

	const handleSend = async () => {
		if (!input.trim()) return

		// Добавляем сообщение пользователя
		const userMessage = { type: 'user', content: input }
		setMessages(prev => [...prev, userMessage])

		setInput('')
		setLoading(true)

		try {
			const response = await fetch('http://localhost:8000/ask', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ prompt: userMessage.content }),
			})

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`)
			}

			const data = await response.json()

			const botMessage = {
				type: 'bot',
				content: data.content || '',
				sources: data.sources || [],
			}

			setMessages(prev => [...prev, botMessage])
		} catch (error) {
			console.error('Ошибка при запросе:', error)

			// Если ошибка, тоже показываем её как сообщение бота
			const errorMessage = {
				type: 'bot',
				content: 'Произошла ошибка при получении ответа.',
				sources: [error.message],
			}
			setMessages(prev => [...prev, errorMessage])
		} finally {
			setLoading(false)
		}
	}

	return (
		<div style={{ padding: '1rem' }}>
			<div style={{ marginBottom: '1rem' }}>
				{messages.map((msg, idx) => (
					<div
						key={idx}
						style={{ textAlign: msg.type === 'user' ? 'left' : 'right' }}
					>
						<p>{msg.content}</p>
						{msg.sources &&
							msg.sources.length > 0 &&
							msg.sources.map((s, i) => (
								<div key={i} className='source'>
									{s}
								</div>
							))}
					</div>
				))}
			</div>

			<div>
				<input
					type='text'
					value={input}
					onChange={e => setInput(e.target.value)}
					onKeyDown={e => e.key === 'Enter' && handleSend()}
					disabled={loading}
				/>
				<button onClick={handleSend} disabled={loading}>
					Отправить
				</button>
			</div>
		</div>
	)
}

export default ChatBot
