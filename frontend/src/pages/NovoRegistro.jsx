import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import api from '../services/api'

export default function NovoRegistro() {
  const navigate = useNavigate()
  const location = useLocation()
  const ID_VEICULO = 1
  const odometroAnterior = location.state?.odometroAnterior || ''

  const [form, setForm] = useState({
    id_tanque: 1,
    id_combustivel: null,
    tipo: 'abastecimento',
    data: new Date().toISOString().slice(0, 16), // Formato para datetime-local
    odometro: odometroAnterior, 
    quantidade: '',
    valor_total: '',
    valor_unitario: '',
    tanque_cheio: false, // Checar se for preenchido 100% no percentual do tanque ou da bateria
    percentual_tanque: '', // Não está preenchendo quando clica no tanque cheio, apenas se for alterado o tanque
    percentual_bateria: '', // Não está preenchendo quando clica no tanque cheio, apenas se for alterado o tanque
    observacao: ''
  })

  const [salvando, setSalvando] = useState(false)
  const [erro, setErro] = useState(null)

  // Buscar o último registro para preencher o odômetro inicial e para verificação se o odometro informado é menor que o último registro
  {/*useEffect(() => {
    async function buscarUltimoOdometro() {
      try {
        const response = await api.get(`/registros/ultimo/${ID_VEICULO}`)
        setForm(prev => ({
          ...prev,
          odometro: response.data.odometro
        }))
      } catch (error) {
        console.error('Erro ao buscar último registro:', error)
      }
    }

    buscarUltimoOdometro()
  }, [ID_VEICULO]) */}


  function handleChange(e) {
    const { name, value, type, checked } = e.target
    const newValue = type === 'checkbox' ? checked : value
    
    setForm(prev => {
      let updatedForm = { ...prev, [name]: newValue }

      if (name === 'quantidade' && newValue !== '') {
        if (updatedForm.valor_unitario !== '') {
          updatedForm.valor_total = (parseFloat(newValue) * parseFloat(updatedForm.valor_unitario)).toFixed(2)
        } else if (updatedForm.valor_total !== '') {
        updatedForm.valor_unitario = (parseFloat(updatedForm.valor_total) / parseFloat(newValue || 1)).toFixed(4)
        }
      }
      else if (name === 'valor_unitario' && newValue !== '') {
        if (updatedForm.quantidade !== '') {
          updatedForm.valor_total = (parseFloat(updatedForm.quantidade) * parseFloat(newValue)).toFixed(2)
        } else if (updatedForm.valor_total !== '') {
          updatedForm.quantidade = (parseFloat(updatedForm.valor_total) / parseFloat(newValue)).toFixed(3)
        }
      }
      else if (name === 'valor_total' && newValue !== '') {
        if (updatedForm.quantidade !== '' && parseFloat(updatedForm.quantidade) !== 0) {
          updatedForm.valor_unitario = (parseFloat(newValue) / parseFloat(updatedForm.quantidade)).toFixed(4)
        } else if (updatedForm.valor_unitario !== '' && parseFloat(updatedForm.valor_unitario) !== 0) {
          updatedForm.quantidade = (parseFloat(newValue) / parseFloat(updatedForm.valor_unitario)).toFixed(3)
        }
      }

      // Se marcar tanque cheio, preencher automaticamente o percentual do tanque ou da bateria dependendo do tipo de tanque
      if (name === 'tanque_cheio' && newValue === true) {
        if (updatedForm.id_tanque === '1') {
          updatedForm.percentual_bateria = 100
        } else if (updatedForm.id_tanque === '2') {
          updatedForm.percentual_tanque = 100
        }
      }
      // Se desmarcar tanque cheio, limpar os percentuais
      else if (name === 'tanque_cheio' && newValue === false) {
        if (updatedForm.id_tanque === '1') {
          updatedForm.percentual_bateria = ''
        } else if (updatedForm.id_tanque === '2') {
          updatedForm.percentual_tanque = ''
        }
      }
      // Se mudar o tipo de tanque enquanto tanque cheio estiver marcado, atualizar os percentuais
      else if (name === 'id_tanque' && updatedForm.tanque_cheio) {
        if (newValue === '1') {
          updatedForm.percentual_bateria = 100
          updatedForm.percentual_tanque = ''
        } else if (newValue === '2') {
          updatedForm.percentual_tanque = 100
          updatedForm.percentual_bateria = ''
        }
      }

      return updatedForm
    }
    )
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSalvando(true)
    setErro(null)

    try {
      const payload = {
        ...form,
        id_tanque: Number(form.id_tanque),
        odometro: Number(form.odometro),
        quantidade: form.quantidade ? Number(form.quantidade) : null,
        valor_total: form.valor_total ? Number(form.valor_total) : null,
        valor_unitario: form.valor_unitario ? Number(form.valor_unitario) : null,
        percentual_tanque: form.percentual_tanque ? Number(form.percentual_tanque) : null,
        percentual_bateria: form.percentual_bateria ? Number(form.percentual_bateria) : null,
        data: new Date(form.data).toISOString()
      }

      await api.post(`/registros/?id_veiculo=${ID_VEICULO}`, payload)
      navigate('/registros')
    } catch (error) {
      setErro('Erro ao salvar registro. Verifique os dados e tente novamente.')
      console.error(error)
    } finally {
      setSalvando(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="flex items-center gap-3 mb-6">
        <button onClick={() => navigate('/registros')} className="text-gray-500 hover:text-gray-700">
          ← Voltar
        </button>
        <h1 className="text-2xl font-bold">Novo Registro</h1>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">

        <div>
          <label className="block text-sm font-medium mb-1">Tipo</label>
          <select name="tipo" value={form.tipo} onChange={handleChange}
            className="w-full border rounded-lg p-2">
            <option value="abastecimento">Abastecimento</option>
            <option value="checkpoint">Checkpoint</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Tanque</label>
          <select name="id_tanque" value={form.id_tanque} onChange={handleChange}
            className="w-full border rounded-lg p-2">
            <option value={1}>Elétrico</option>
            <option value={2}>Combustível</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Data e hora</label>
          <input type="datetime-local" name="data" value={form.data} onChange={handleChange}
            className="w-full border rounded-lg p-2" required />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Odômetro (km)</label>
          <input type="number" name="odometro" value={form.odometro} onChange={handleChange}
            className="w-full border rounded-lg p-2" required />
        </div>

        {form.tipo === 'abastecimento' && (
          <>
            <div>
              <label className="block text-sm font-medium mb-1">Quantidade (kWh ou L)</label>
              <input type="number" step="0.001" name="quantidade" value={form.quantidade} onChange={handleChange}
                className="w-full border rounded-lg p-2" />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Valor total (R$)</label>
              <input type="number" step="0.01" name="valor_total" value={form.valor_total} onChange={handleChange}
                className="w-full border rounded-lg p-2" />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Valor unitário (R$/L ou R$/kWh)</label>
              <input type="number" step="0.0001" name="valor_unitario" value={form.valor_unitario} onChange={handleChange}
                className="w-full border rounded-lg p-2" />
            </div>

            <div className="flex items-center gap-2">
              <input type="checkbox" name="tanque_cheio" checked={form.tanque_cheio} onChange={handleChange}
                className="w-4 h-4" />
              <label className="text-sm font-medium">Tanque cheio</label>
            </div>
          </>
        )}

        <div>
          <label className="block text-sm font-medium mb-1">% Bateria</label>
          <input type="number" min="0" max="100" name="percentual_bateria" value={form.percentual_bateria} onChange={handleChange}
            className="w-full border rounded-lg p-2" disabled={form.tanque_cheio && form.id_tanque === '1'} />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">% Tanque combustível</label>
          <input type="number" min="0" max="100" name="percentual_tanque" value={form.percentual_tanque} onChange={handleChange}
            className="w-full border rounded-lg p-2" disabled={form.tanque_cheio && form.id_tanque === '2'} />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Observação</label>
          <textarea name="observacao" value={form.observacao} onChange={handleChange}
            className="w-full border rounded-lg p-2" rows={3} />
        </div>

        {erro && <p className="text-red-500 text-sm">{erro}</p>}

        <button type="submit" disabled={salvando}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50">
          {salvando ? 'Salvando...' : 'Salvar registro'}
        </button>

      </form>
    </div>
  )
}