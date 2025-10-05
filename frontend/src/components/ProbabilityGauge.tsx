import { Pie, PieChart, ResponsiveContainer, Cell } from 'recharts';

interface ProbabilityGaugeProps {
  probability: number; // 0-1
}

const COLORS = ['#0ea5e9', '#1e293b'];

export function ProbabilityGauge({ probability }: ProbabilityGaugeProps) {
  const data = [
    { name: 'Rain', value: probability },
    { name: 'Dry', value: 1 - probability }
  ];

  return (
    <div className="w-full h-48">
      <ResponsiveContainer>
        <PieChart>
          <Pie data={data} innerRadius="60%" outerRadius="80%" paddingAngle={2} dataKey="value">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div className="text-center mt-2 text-3xl font-bold">
        {(probability * 100).toFixed(0)}%
      </div>
      <p className="text-center text-sm text-slate-300">Chance of measurable rain</p>
    </div>
  );
}
