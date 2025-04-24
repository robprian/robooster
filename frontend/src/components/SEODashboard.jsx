import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';

const SEODashboard = () => {
  const [urls, setUrls] = useState([
    {
      id: 1,
      url: 'https://example.com',
      score: 85,
      status: 'indexed',
      lastChecked: '2024-01-20',
      issues: ['Meta description too short', 'Missing alt tags']
    }
  ]);

  const [newUrl, setNewUrl] = useState('');

  const handleAddUrl = () => {
    if (!newUrl) return;
    // TODO: Implement API call to analyze URL
    setUrls([...urls, {
      id: urls.length + 1,
      url: newUrl,
      score: 0,
      status: 'pending',
      lastChecked: new Date().toISOString().split('T')[0],
      issues: []
    }]);
    setNewUrl('');
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="p-6 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>SEO Dashboard</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4 mb-6">
            <Input
              placeholder="Masukkan URL untuk analisis"
              value={newUrl}
              onChange={(e) => setNewUrl(e.target.value)}
            />
            <Button onClick={handleAddUrl}>Analisis URL</Button>
          </div>

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>URL</TableHead>
                <TableHead>Skor SEO</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Terakhir Dicek</TableHead>
                <TableHead>Masalah</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {urls.map((url) => (
                <TableRow key={url.id}>
                  <TableCell className="font-medium">{url.url}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Progress
                        value={url.score}
                        className={`w-[60px] ${getScoreColor(url.score)}`}
                      />
                      <span>{url.score}%</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge
                      variant={url.status === 'indexed' ? 'success' : 'warning'}
                    >
                      {url.status}
                    </Badge>
                  </TableCell>
                  <TableCell>{url.lastChecked}</TableCell>
                  <TableCell>
                    <div className="flex flex-wrap gap-1">
                      {url.issues.map((issue, index) => (
                        <Badge key={index} variant="secondary">
                          {issue}
                        </Badge>
                      ))}
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default SEODashboard;