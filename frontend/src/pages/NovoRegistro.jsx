import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function NovoRegistro() {
  const navigate = useNavigate()
  const ID_VEICULO = 1

  const [form, setForm] = useState({
    id_tanque: 1,
    id_combustivel: null,
    tipo: 'abastecimento',
    data: new Date().toISOString().slice(0, 16),
    odometro: '',
    quantidade: '',
    valor_total: '',
    valor_unitario: '',
    tanque_cheio: false,
    percentual_tanque: '',
    percentual_bateria: '',
    observacao: ''
  })

  const [salvando, setSalvando] = useState(false)
  const [erro, setErro] = useState(null)

  function handleChange(e) {
    const { name, value, type, checked } = e.target
    setForm(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
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
            className="w-full border rounded-lg p-2" />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">% Tanque combustível</label>
          <input type="number" min="0" max="100" name="percentual_tanque" value={form.percentual_tanque} onChange={handleChange}
            className="w-full border rounded-lg p-2" />
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